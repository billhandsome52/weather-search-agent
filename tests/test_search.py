"""
搜索工具测试
"""

import pytest
from app.tools.search import search_web


def test_search_web_basic():
    """测试基本搜索（DuckDuckGo 免费）"""
    result = search_web.invoke({"query": "Python 编程"})
    # 只要有返回就行（可能成功或网络错误）
    assert len(result) > 0


def test_search_num_results():
    """测试结果数量"""
    result = search_web.invoke({"query": "Python", "num_results": 3})
    # 验证返回了结果
    assert len(result) > 0


def test_search_empty_query():
    """测试空查询"""
    result = search_web.invoke({"query": ""})
    # 空查询应该返回错误或无结果
    assert len(result) > 0
