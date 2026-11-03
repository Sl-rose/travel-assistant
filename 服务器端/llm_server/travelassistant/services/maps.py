import os
import httpx
import asyncio
from django.conf import settings

AMAP_KEY = getattr(settings, "AMAP_API_KEY", None) or os.getenv("AMAP_API_KEY")

async def get_location_coordinate(address: str):
    """将地名转换为经纬度坐标"""
    if not AMAP_KEY:
        print("[错误] 高德地图API密钥未配置")
        return None
    
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": AMAP_KEY,
        "address": address
    }
    
    print(f"[DEBUG] 使用API Key: {AMAP_KEY[:10]}...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()
            # --- 关键：打印原始数据 ---
            print(f"\n[DEBUG 地理编码] 查询地址: {address}")
            print(f"[DEBUG 地理编码] 原始返回内容: {data}")
            
            # 检查API状态
            if data.get("status") == "0":
                error_info = data.get("info", "未知错误")
                error_code = data.get("infocode", "")
                print(f"[错误] 地理编码失败: {error_info} (错误码: {error_code})")
                
                # 针对AP010010错误的特殊处理
                if error_code == "AP010010":
                    print(f"[提示] 地址 '{address}' 无法识别，请尝试更详细的地址描述")
                    print(f"[建议] 例如：'上海外滩' 改为 '上海市黄浦区外滩'")
                
                return None
            
            # 检查是否有结果
            if data.get("status") == "1" and data.get("geocodes") and len(data["geocodes"]) > 0:
                location = data["geocodes"][0]["location"]
                print(f"[成功] 坐标获取成功: {location}")
                return location
            else:
                print(f"[警告] 未找到地址 '{address}' 的坐标信息")
                return None
        except Exception as e:
            print(f"[错误] 网络请求出错: {e}")
            return None

async def search_nearby_poi(location: str, keywords: str):
    """搜索周边景点或餐厅"""
    url = "https://restapi.amap.com/v3/place/around"
    params = {
        "key": AMAP_KEY,
        "location": location,
        "keywords": keywords,
        "radius": 3000,
        "offset": 5
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()
            # --- 关键：打印原始数据 ---
            print(f"\n[DEBUG 周边搜索] 原始返回内容: {data}")
            return data
        except Exception as e:
            return {"error": str(e)}

if __name__ == '__main__':
    async def test():
        target = "上海外滩"
        print(f"--- 正在测试: {target} ---")
        
        coord = await get_location_coordinate(target)
        
        if coord:
            print(f"坐标获取成功: {coord}")
            print("\n--- 正在发起周边搜索 ---")
            await search_nearby_poi(coord, "景点")
        else:
            print("\n[!] 无法获取坐标，请查看上方的 DEBUG 原始返回内容定位原因。")

    asyncio.run(test())