"""
Agent 构建模块 - 使用 LangGraph
"""

from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

from app.config import settings
from app.tools import get_weather, search_web


def create_llm() -> ChatOpenAI:
    """创建 LLM 实例"""
    if settings.dashscope_api_key:
        # 使用阿里云百炼 (DashScope)
        return ChatOpenAI(
            model=settings.default_llm_model,
            api_key=settings.dashscope_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.7,
        )
    elif settings.openai_api_key:
        # 使用 OpenAI
        return ChatOpenAI(
            model=settings.default_llm_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )
    else:
        raise ValueError("未配置 LLM API Key，请设置 DASHSCOPE_API_KEY 或 OPENAI_API_KEY")


# 全局 Agent 实例
_agent = None
_memory = None


def get_agent(verbose: bool = False):
    """获取或创建全局 Agent 实例"""
    global _agent, _memory
    
    if _agent is None:
        # 创建 LLM
        llm = create_llm()
        
        # 定义工具
        tools = [get_weather, search_web]
        
        # 创建记忆存储
        _memory = MemorySaver()
        
        # 创建系统提示
        system_prompt = """你是一个乐于助人的 AI 助手，名字叫 Bill。
你可以帮用户查询天气和搜索网页信息。

可用工具：
- get_weather(city, days): 查询城市天气
- search_web(query, num_results): 搜索网页

请用友好、简洁的中文回答。如果工具调用失败，请友好地告知用户。"""
        
        # 创建 ReAct Agent
        _agent = create_react_agent(
            llm,
            tools,
            prompt=system_prompt,
            checkpointer=_memory,
        )
        
        if verbose:
            print("✅ Agent 初始化成功")
    
    return _agent, _memory


def invoke_agent(message: str, session_id: str = "default") -> Dict[str, Any]:
    """
    调用 Agent
    
    Args:
        message: 用户输入
        session_id: 会话 ID
    
    Returns:
        包含输出的字典
    """
    agent, memory = get_agent()
    
    # 配置会话
    config = {"configurable": {"thread_id": session_id}}
    
    # 调用 Agent
    result = agent.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config,
    )
    
    # 获取最后一条消息（AI 回答）
    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        return {"output": last_message.content}
    
    return {"output": "抱歉，我无法回答这个问题"}
