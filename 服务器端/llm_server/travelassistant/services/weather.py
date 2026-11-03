import json
import os
from urllib.request import urlopen
from urllib.parse import urlencode
from django.conf import settings

API_KEY = getattr(settings, "WEATHER_API_KEY", None) or os.environ.get("WEATHER_API_KEY")

def get_weather_info(location:str):
    
    params = {
        "key": API_KEY,
        "location": location,
        "language": "zh-Hans",
        "unit": "c"
    }
    
    url = "https://api.seniverse.com/v3/weather/now.json?" + urlencode(params)
    
    try:
        with urlopen(url) as response:
            return json.load(response)
    except Exception as e:
        if hasattr(e, 'fp'):
            print(f"错误详情: {e.fp.read().decode()}")
        return {"error": str(e)}

if __name__ == '__main__':
    # 36:118 是经纬度格式
    result = get_weather_info("36:118")
    print(json.dumps(result, indent=2, ensure_ascii=False))