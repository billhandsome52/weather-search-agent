"""
搜索工具测试
"""

import pytest
from app.tools.search import search_web
from app.config import settings


def test_search_requires_api_key():
    """测试搜索需要 API Key"""
    if not settings.brave_api_key:
        result = search_web.invoke({"query": "test"})
        assert "未配置" in result or "API Key" in result


@pytest.mark.skipif(not settings.brave_api_key, reason="需要 Brave API Key")
def test_search_web_basic():
    """测试基本搜索"""
    result = search_web.invoke({"query": "Python 编程"})
    assert "搜索结果" in result or "Python" in result


@pytest.mark.skipif(not settings.brave_api_key, reason="需要 Brave API Key")
def test_search_num_results():
    """测试结果数量"""
    result = search_web.invoke({"query": "test", "num_results": 3})
    # 验证返回了结果
    assert len(result) > 0
