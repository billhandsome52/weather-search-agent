"""
天气查询工具 - 使用 Open-Meteo API (免费，无需 API Key)
文档：https://open-meteo.com/
"""

import httpx
from typing import Optional
from langchain_core.tools import tool


# 主要城市的经纬度（简化版，实际生产应该用地理编码 API）
CITY_COORDINATES = {
    "上海": (31.2304, 121.4737),
    "北京": (39.9042, 116.4074),
    "深圳": (22.5431, 114.0579),
    "广州": (23.1291, 113.2644),
    "杭州": (30.2741, 120.1551),
    "成都": (30.5728, 104.0668),
    "南京": (32.0603, 118.7969),
    "武汉": (30.5928, 114.3055),
    "西安": (34.3416, 108.9398),
    "重庆": (29.5630, 106.5516),
    "东京": (35.6762, 139.6503),
    "纽约": (40.7128, -74.0060),
    "伦敦": (51.5074, -0.1278),
    "巴黎": (48.8566, 2.3522),
    "新加坡": (1.3521, 103.8198),
}


def get_city_coordinates(city: str) -> Optional[tuple[float, float]]:
    """获取城市经纬度"""
    # 先尝试精确匹配
    if city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    
    # 尝试模糊匹配
    city_lower = city.lower()
    for name, coords in CITY_COORDINATES.items():
        if city_lower in name.lower() or name.lower() in city_lower:
            return coords
    
    return None


@tool
def get_weather(city: str, days: int = 1) -> str:
    """
    查询指定城市的天气信息
    
    Args:
        city: 城市名称，如"上海"、"北京"、"Tokyo"
        days: 查询天数（1-7），默认 1 天
    
    Returns:
        天气信息字符串，包含温度、天气状况、风速等
    """
    coords = get_city_coordinates(city)
    
    if not coords:
        return f"抱歉，暂未支持城市 '{city}' 的天气查询。支持的城市包括：{', '.join(list(CITY_COORDINATES.keys())[:10])}..."
    
    lat, lon = coords
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                    "forecast_days": min(days, 7),
                    "timezone": "auto",
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # 解析当前天气
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        # 天气代码映射
        weather_codes = {
            0: "晴",
            1: "主要晴朗",
            2: "部分多云",
            3: "多云",
            45: "雾",
            48: "雾凇",
            51: "毛毛雨",
            53: "中度毛毛雨",
            55: "密集毛毛雨",
            61: "小雨",
            63: "中雨",
            65: "大雨",
            71: "小雪",
            73: "中雪",
            75: "大雪",
            80: "小阵雨",
            81: "中阵雨",
            82: "大阵雨",
            95: "雷雨",
            96: "雷阵雨",
            99: "强雷阵雨",
        }
        
        def get_weather_desc(code: int) -> str:
            return weather_codes.get(code, "未知")
        
        # 构建结果
        result = []
        result.append(f"📍 {city} 天气信息")
        result.append("-" * 30)
        
        if current:
            temp = current.get("temperature_2m", "N/A")
            humidity = current.get("relative_humidity_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")
            weather = get_weather_desc(current.get("weather_code", -1))
            
            result.append(f"当前：{weather} {temp}°C")
            result.append(f"湿度：{humidity}%")
            result.append(f"风速：{wind} km/h")
        
        if daily:
            result.append("")
            result.append("预报:")
            for i, date in enumerate(daily.get("time", [])[:days]):
                max_temp = daily.get("temperature_2m_max", [])[i] if i < len(daily.get("temperature_2m_max", [])) else "N/A"
                min_temp = daily.get("temperature_2m_min", [])[i] if i < len(daily.get("temperature_2m_min", [])) else "N/A"
                weather = get_weather_desc(daily.get("weather_code", [])[i] if i < len(daily.get("weather_code", [])) else -1)
                result.append(f"  {date}: {weather} {min_temp}°C ~ {max_temp}°C")
        
        return "\n".join(result)
    
    except httpx.TimeoutException:
        return "天气查询超时，请稍后重试"
    except Exception as e:
        return f"天气查询失败：{str(e)}"


if __name__ == "__main__":
    # 测试
    print(get_weather.invoke({"city": "上海"}))
    print("\n")
    print(get_weather.invoke({"city": "北京", "days": 3}))
