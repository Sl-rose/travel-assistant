# 大模型用到的包
import os
from openai import OpenAI
class QwenLLM:
    def __init__(self):
        self.client = OpenAI(
            # 获取环境变量的apikey
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            # 请求地址
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    def inference(self,message=[],model="qwen-plus",stream=False,enable_search=False,enable_thinking=False):
        try:
            completion = self.client.chat.completions.create(
                # 模型名称
                model=model, 
                # 对话内容
                messages=message,
                # 流式输出
                stream=stream,
                # 扩展配置
                extra_body = {"enable_search":bool(enable_search),
                              "enable_thinking":bool(enable_thinking)
                }
            )
            # 非流式
            if not stream:
                answer = completion.choices[0].message.content
                return answer
            # 流式
            return completion
        except Exception as e:
            print(f"错误信息：{e}")
            return f"错误信息：{e}"