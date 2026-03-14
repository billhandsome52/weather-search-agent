"""
网页搜索工具 - 使用 DuckDuckGo（免费，无需 API Key）
文档：https://pypi.org/project/duckduckgo-search/
"""

from typing import List
from langchain_core.tools import tool


@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    搜索互联网信息（使用 DuckDuckGo，免费无需 API Key）
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量（1-10），默认 5
    
    Returns:
        搜索结果字符串，包含标题、摘要和链接
    """
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return "⚠️ 缺少依赖：请运行 `poetry add duckduckgo-search` 安装"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=min(num_results, 10)))
        
        if not results:
            return f"未找到关于 '{query}' 的搜索结果"
        
        result = []
        result.append(f"🔍 搜索结果：'{query}'")
        result.append("-" * 40)
        
        for i, item in enumerate(results, 1):
            title = item.get("title", "无标题")
            body = item.get("body", "无摘要")
            url = item.get("href", "")
            
            result.append(f"\n{i}. {title}")
            result.append(f"   {body}")
            result.append(f"   🔗 {url}")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"搜索失败：{str(e)}"


if __name__ == "__main__":
    # 测试
    print(search_web.invoke({"query": "Python 异步编程"}))
