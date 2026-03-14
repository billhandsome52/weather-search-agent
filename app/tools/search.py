"""
网页搜索工具 - 使用 Brave Search API
文档：https://brave.com/search/api/
"""

import httpx
from typing import List
from langchain_core.tools import tool
from app.config import settings


@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    搜索互联网信息
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量（1-10），默认 5
    
    Returns:
        搜索结果字符串，包含标题、摘要和链接
    """
    brave_api_key = settings.brave_api_key
    
    if not brave_api_key:
        return "⚠️ 搜索功能未配置：请在 .env 文件中设置 BRAVE_API_KEY\n获取 API Key: https://brave.com/search/api/"
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={
                    "Accept": "application/json",
                    "X-Subscription-Token": brave_api_key,
                },
                params={
                    "q": query,
                    "count": min(num_results, 10),
                    "text_decorations": False,
                }
            )
            response.raise_for_status()
            data = response.json()
        
        web_results = data.get("web", {}).get("results", [])
        
        if not web_results:
            return f"未找到关于 '{query}' 的搜索结果"
        
        result = []
        result.append(f"🔍 搜索结果：'{query}'")
        result.append("-" * 40)
        
        for i, item in enumerate(web_results, 1):
            title = item.get("title", "无标题")
            description = item.get("description", "无摘要")
            url = item.get("url", "")
            
            result.append(f"\n{i}. {title}")
            result.append(f"   {description}")
            result.append(f"   🔗 {url}")
        
        return "\n".join(result)
    
    except httpx.TimeoutException:
        return "搜索超时，请稍后重试"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "⚠️ Brave API Key 无效，请检查 .env 配置"
        elif e.response.status_code == 429:
            return "⚠️ 搜索请求超限，请稍后重试"
        return f"搜索失败：{str(e)}"
    except Exception as e:
        return f"搜索失败：{str(e)}"


if __name__ == "__main__":
    # 测试
    print(search_web.invoke({"query": "Python 异步编程"}))
