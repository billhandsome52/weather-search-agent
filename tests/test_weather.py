"""
天气工具测试
"""

import pytest
from app.tools.weather import get_weather, get_city_coordinates, CITY_COORDINATES


def test_get_city_coordinates_known():
    """测试已知城市坐标"""
    coords = get_city_coordinates("上海")
    assert coords is not None
    assert coords[0] == 31.2304  # latitude
    assert coords[1] == 121.4737  # longitude


def test_get_city_coordinates_unknown():
    """测试未知城市"""
    coords = get_city_coordinates("UnknownCity12345")
    assert coords is None


def test_get_weather_shanghai():
    """测试上海天气查询"""
    result = get_weather.invoke({"city": "上海"})
    assert "上海" in result
    assert "温度" in result or "气温" in result or "°C" in result


def test_get_weather_beijing():
    """测试北京天气查询"""
    result = get_weather.invoke({"city": "北京"})
    assert "北京" in result


def test_get_weather_invalid_city():
    """测试无效城市"""
    result = get_weather.invoke({"city": "InvalidCityXYZ123"})
    assert "暂未支持" in result or "抱歉" in result


def test_city_coordinates_coverage():
    """测试城市覆盖"""
    expected_cities = ["上海", "北京", "深圳", "广州", "东京", "纽约"]
    for city in expected_cities:
        assert city in CITY_COORDINATES, f"城市 {city} 不在坐标字典中"
