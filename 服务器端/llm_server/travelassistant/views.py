from django.http import JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage
from urllib.parse import unquote
from django.conf import settings

import base64
import os
import re
import asyncio

# RAG系统的导入
from utils.RAGSystem import RAGSystem


# 处理图片过大的包
from PIL import Image
import io

#保证文件名唯一性
import uuid

# 导入大模型处理的包
from utils.QwenLLM import QwenLLM
qwen = QwenLLM()

# 数据库操作模型导入
from .models import Topic,ChatMessage
from django.utils import timezone

# 导入提示词
from utils.prompt import SUMMARY_PROMPT,HISTORY_SUMMARY_PROMPT,HISTORY_SYSTEM_PROMPT,LONGMEMORY_PROMPT
import json
from .services.weather import get_weather_info
from .services.maps import get_location_coordinate, search_nearby_poi


def get_request_userid(request):
    user = getattr(request, "user", None)
    if isinstance(user, dict):
        return user.get("userid")
    return None


def extract_city_for_weather(query):
    match = re.search(r"([\u4e00-\u9fa5]{2,20})(?:的)?(?:天气|气温)", query)
    return match.group(1) if match else ""


def detect_poi_keyword(query):
    keyword_map = [
        ("景点", ["景点", "景区", "好玩", "游玩"]),
        ("美食", ["美食", "吃", "餐厅", "小吃"]),
        ("酒店", ["酒店", "住宿", "旅馆"]),
    ]
    for keyword, words in keyword_map:
        if any(word in query for word in words):
            return keyword
    return "景点"


def extract_place_for_poi(query):
    # 改进正则，支持更多模式
    patterns = [
        # 模式1: 明确的地名（带行政区划）
        r"(?:在|到|去|找|搜|查询)?([\u4e00-\u9fa5]{2,6}(?:省|市|区|县|镇|村))([\u4e00-\u9fa5]{2,20}(?:路|街|道|广场|公园|站|机场|景区|景点))?(?:附近|周边|周围|旁边)?",
        # 模式2: 地名+附近
        r"(?:在|到|去|找|搜|查询)?([\u4e00-\u9fa5]{2,30})(?:附近|周边|周围|旁边)",
        # 模式3: 知名地标
        r"(?:在|到|去|找|搜|查询)?([\u4e00-\u9fa5]{2,30}(?:广场|公园|站|机场|景区|景点|大学|医院|商场|酒店))(?:附近|周边|周围|旁边)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            # 组合完整的地址
            place = ''.join([g for g in match.groups() if g]).strip()
            # 过滤掉无效的地名
            if place and len(place) >= 2:
                print(f"[DEBUG] 提取到地址: {place}")
                return place
    print(f"[DEBUG] 未能从查询中提取地址: {query}")
    return ""


def build_realtime_context(query):
    """
    根据用户问题尝试调用实时服务（天气/附近POI），返回可注入LLM的上下文文本。
    """
    context_parts = []
    is_weather_query = ("天气" in query) or ("气温" in query)
    is_nearby_query = ("附近" in query or "周边" in query) and any(x in query for x in ["景点", "景区", "美食", "餐厅", "酒店", "住宿", "好玩"])

    if is_weather_query:
        city = extract_city_for_weather(query)
        if city:
            weather_data = get_weather_info(city)
            if isinstance(weather_data, dict) and weather_data.get("results"):
                now_info = weather_data["results"][0].get("now", {})
                location_info = weather_data["results"][0].get("location", {})
                print(
                    f"[实时服务] 天气调用成功 city={location_info.get('name', city)} "
                    f"text={now_info.get('text', '未知')} temp={now_info.get('temperature', '未知')}"
                )
                weather_text = (
                    f"实时天气：城市={location_info.get('name', city)}，"
                    f"天气={now_info.get('text', '未知')}，"
                    f"温度={now_info.get('temperature', '未知')}摄氏度。"
                )
                context_parts.append(weather_text)

    if is_nearby_query:
        place = extract_place_for_poi(query)
        poi_keyword = detect_poi_keyword(query)
        if place:
            try:
                location = asyncio.run(get_location_coordinate(place))
                if location and not isinstance(location, str):
                    print(f"[实时服务] 地图地理编码成功 place={place} location={location}")
                    poi_data = asyncio.run(search_nearby_poi(location, poi_keyword))
                    pois = poi_data.get("pois", []) if isinstance(poi_data, dict) else []
                    if pois:
                        print(
                            f"[实时服务] 地图POI调用成功 place={place} keyword={poi_keyword} "
                            f"count={len(pois)}"
                        )
                        top_pois = pois[:5]
                        poi_lines = []
                        for poi in top_pois:
                            poi_lines.append(
                                f"{poi.get('name', '未知地点')}（地址：{poi.get('address', '未知')}，"
                                f"距离约{poi.get('distance', '未知')}米）"
                            )
                        context_parts.append(
                            f"附近{poi_keyword}实时检索结果（参考地点：{place}）：" + "；".join(poi_lines)
                        )
            except Exception as e:
                print("实时POI查询失败:", e)

    return "\n".join(context_parts).strip()


def encode_image(image_path):
    if not os.path.exists(image_path):
        return None
    
    # 打开图片
    with Image.open(image_path) as img:
        # 如果图片像素过大，进行等比例缩放（例如最大宽度不超过 2000 像素）
        max_size = 2000
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size))
        
        # 将处理后的图片保存到内存中，并压缩质量
        buffer = io.BytesIO()
        # 转换为 RGB 模式（防止 RGBA 报错），保存为 JPEG，质量设为 75
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        img.save(buffer, format="JPEG", quality=75)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

@csrf_exempt
def deltopic(request):
    topicid = request.GET.get("topicid",0)
    userid = get_request_userid(request) or request.GET.get("userid", 0)
    # 删除主题
    Topic.objects.filter(id=topicid,userid=userid).update(is_deleted=1)
    # 删除聊天记录
    ChatMessage.objects.filter(topicid=topicid,userid=userid).update(is_deleted=1,deleted=timezone.now())
    return JsonResponse({"status":"success"})
    
@csrf_exempt
def detail(request):
    topicid = request.GET.get("topicid",0)
    userid = get_request_userid(request) or request.GET.get("userid", 0)
    # 获取一条记录
    info = ChatMessage.objects.filter(topicid=topicid,userid=userid,is_deleted=0)
    # 数据处理
    chatlist = [{"role":chat.role,"content":chat.content} for chat in info]
    return JsonResponse({"status":"success","chat":chatlist})
# 历史记录试图
@csrf_exempt
def history(request):
    userid = get_request_userid(request) or request.GET.get("userid", 0)
    # 获取历史主题列表
    historylist = Topic.objects.filter(userid=userid,is_deleted=0).order_by("-created_at")
    historylist = [
        {
            "topicid":history.id,
            "title":history.title,
            "created_at":history.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for history in historylist
    ]
    # 响应数据搭配客户端
    return JsonResponse({"status":"success","historylist":historylist})

@csrf_exempt
def assistant(request):
    rag = RAGSystem()
    userid = get_request_userid(request) or request.POST.get("userid", 0)
    query = request.POST.get("query", "").strip()
    
    enable_search = int(request.POST.get("web", 0))
    enable_thinking = int(request.POST.get("deepthink", 0))
    image_url = request.POST.get("file_url", "")
    topicid = int(request.POST.get("topicid", 0))

    now_local = timezone.localtime()
    time_context = now_local.strftime("%Y-%m-%d %H:%M:%S")
    weekday_map = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日",
    }
    weekday_text = weekday_map.get(now_local.weekday(), "")

    messages = [
            {
                'role': 'system',
                'content': (
                    "你非常擅长处理旅游相关问题。"
                    f"当前本地时间为：{time_context}（{weekday_text}）。"
                    "当用户提问涉及今天/明天/近期计划时，请基于该时间理解。"
                )
            },
    ]
    
    # 2. 处理主题 ID（保持同一个聊天框同一个 ID）
    if topicid == 0:
        # 只有第一句话才生成标题并创建新主题
        prompt = f"""
            {SUMMARY_PROMPT}
            query:{query}\n
        """
        
        summary = qwen.inference([{"role": "user", "content": prompt}])
        print(f'生成的标题：{summary}')
        
        topic = Topic.objects.create(userid=userid, title=summary, created_at=timezone.now())
        topicid = topic.id
    else:
        start_count = 0
        SHORT_MEMORY_COUNT = 6  # 短期记忆数量
        # 读取主题的长期记忆信息以及长度
        topic_info = Topic.objects.get(id=topicid, userid=userid)
        start_count = topic_info.summary_count

        # 到数据库查询历史对话消息
        messages_history = ChatMessage.objects.filter(topicid=topicid, userid=userid, is_deleted=0).order_by("id")
        messages_history = list(messages_history.values())
        
        # 长期记忆做一个摘要
        historyinfo = topic_info.longmemory
        # 累加新的对话以及大模型回答
        new_dialogue = "" #新增对话及大模型回答 
        i, j = start_count // 2, start_count // 2
        for message in messages_history[start_count:-SHORT_MEMORY_COUNT:1]:
            if message.get("role") == 'user':
                i += 1
                new_dialogue += f'问题{i}:{message.get('content')}' + '\n'
            if message.get('role') == 'assistant':
                j += 1
                new_dialogue += f'答案{j}:{message.get('content')}' + '\n'
        print("历史对话信息：",historyinfo)
        if new_dialogue:
            prompt_history = f'''
                {HISTORY_SUMMARY_PROMPT}
                【已有长期记忆】：
                {historyinfo}
                【新增对话】:
                {new_dialogue}
            '''
            longmemory = qwen.inference(
                [
                    {"role": "system","content": HISTORY_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_history},
                ]
            )
            # 保存到数据库
            Topic.objects.filter(id=topicid, userid=userid).update(longmemory=longmemory, summary_count=i + j)

            # messages初始化:加入长期记忆
            longmemory_prompt = f'''
                {LONGMEMORY_PROMPT}
                【长期记忆(只读参考,不可修改)】
                {longmemory}
            '''
            messages = [
                {'role': 'system', 'content': longmemory_prompt},
            ]

        # 短期记忆
        for message in messages_history[-6::]:
            messages.append({"role": message.get("role"), "content": message.get("content")})

    # 用户最新的问题
    query_prompt=query
    # 检索相关知识块
    chunks = rag.retrieval_chunks(query,rank_threshold=0.3)
    if chunks.get("documents"):
        query_prompt += f'''
            请优先结合上下文内容作答；若上下文无相关有效信息，直接独立回答用户问题，
            无需额外说明、无需多余解释,不要说“没有检索到相关信息，无法根据上下文回答。”。
            上下文：{'\n'.join(chunks.get("documents"))}
            Question:{query}
            Response:
        '''
    print("用户的问题：",query_prompt)
    realtime_context = build_realtime_context(query_prompt)
    if realtime_context:
        messages.append({
            "role": "system",
            "content": f"以下是外部实时数据，请优先参考并明确标注为实时信息：\n{realtime_context}"
        })

    model = "qwen-plus"
    if image_url:
        model = "qwen3-vl-plus"
        file_extension = os.path.splitext(image_url)[1]
        print("文件后缀:", file_extension)
        base64_image = encode_image(os.path.join(settings.BASE_DIR, image_url[1:]))
        if base64_image:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                # encode_image 已统一压缩成 JPEG，MIME 需与实际内容一致
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                        {"type": "text", "text": query},
                    ],
                }
            )
        else:
            # 图片读取失败时降级为纯文本，避免多模态请求直接报错
            model = "qwen-plus"
            messages.append({"role": "user", "content": query})
    else:
        messages.append({"role": "user", "content": query_prompt})
    # 保存用户的对话内容
    ChatMessage.objects.create(
        topicid=topicid, 
        userid=userid, 
        role="user", 
        content=query, 
        image_url=image_url,
        created_at=timezone.now()
    )
    # 5. 请求大模型
    response_data = qwen.inference(
        messages, 
        model=model, 
        stream=True, # 流式推理
        enable_search=enable_search, 
        enable_thinking=enable_thinking
    )
    def event_stream():
    # 加了一个异常处理,防止客户端断开连接:前面的代码都应该有一个异常处理
        content = ""
        try:
            # 响应主题的id到客户端
            yield "data: <topic_id_IGCV>" + str(topicid) + "</topic_id_IGCV>\n\n"
            
            for chunk in response_data: # 流式
                if isinstance(chunk, str):
                    safe_content = chunk.replace('\n', '\\n')
                    content += chunk
                    yield f"data: {safe_content}\n\n"
                    continue

                if getattr(chunk, "choices", None):
                    delta = chunk.choices[0].delta or ""
                    if delta and delta.content:
                        # SSE 协议要求:必须以"data:"开头,以两个换行结尾
                        content += delta.content
                        # 将内容中的换行符编码，避免破坏SSE协议格式
                        safe_content = delta.content.replace('\n', '\\n')
                        yield f"data: {safe_content}\n\n"
                        
        except Exception as e:
            print("错误:",e)
        finally:
            # 把元消总响应到客户端
            yield "data:[@#---DONE---#@]\n\n"
            # 6. 存储大模型回答
            ChatMessage.objects.create(
                topicid=topicid, 
                userid=userid, 
                role="assistant", 
                content=content, 
                created_at=timezone.now()
            )
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    # 设置缓存控制:只要有yield产生的数据,就立即响应到客户端,不要缓存
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no" # 禁止Nginx缓冲
    return response

# 接收上传上来的文件
@csrf_exempt
def uploadfile(request):
    file = request.FILES.get("file1")
    if not file:
        return JsonResponse({"status": "fail"})

    # 1. 获取文件的后缀名 (如 .jpg)
    ext = os.path.splitext(file.name)[1]
    
    # 2. 生成一个随机的唯一字符串作为新文件名
    unique_name = f"{uuid.uuid4().hex}{ext}"
    
    fs = FileSystemStorage(
        location=str(settings.BASE_DIR / "static" / "uploads"),
        base_url = settings.STATIC_URL + "uploads/"
    )
    
    # 3. 使用新名字保存
    filename = fs.save(unique_name, file) 
    file_url = fs.url(filename)
    
    return JsonResponse({"status": "success", "file_url": file_url})