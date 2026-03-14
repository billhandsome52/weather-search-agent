"""
Agent 构建模块
"""

from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.tools import tool

from app.config import settings
from app.tools import get_weather, search_web


# 简单的内存存储（生产环境应该用 Redis 等）
chat_histories: Dict[str, ChatMessageHistory] = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    """获取或创建会话历史"""
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]


def create_llm() -> ChatOpenAI:
    """创建 LLM 实例"""
    if settings.dashscope_api_key:
        # 使用阿里云百炼 (DashScope)
        return ChatOpenAI(
            model=settings.default_llm_model,
            openai_api_key=settings.dashscope_api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.7,
        )
    elif settings.openai_api_key:
        # 使用 OpenAI
        return ChatOpenAI(
            model=settings.default_llm_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.7,
        )
    else:
        raise ValueError("未配置 LLM API Key，请设置 DASHSCOPE_API_KEY 或 OPENAI_API_KEY")


def create_agent(verbose: bool = False) -> AgentExecutor:
    """
    创建 Agent
    
    Args:
        verbose: 是否输出详细日志
    
    Returns:
        AgentExecutor 实例
    """
    # 创建 LLM
    llm = create_llm()
    
    # 定义工具
    tools = [get_weather, search_web]
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """你是一个乐于助人的 AI 助手，名字叫 Bill。
你可以帮用户查询天气和搜索网页信息。

可用工具：
- get_weather(city, days): 查询城市天气
- search_web(query, num_results): 搜索网页

请用友好、简洁的中文回答。如果工具调用失败，请友好地告知用户。"""
        ),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建 Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # 创建执行器
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10,
    )
    
    return executor


class AgentChain:
    """带记忆的 Agent 链"""
    
    def __init__(self, verbose: bool = False):
        self.executor = create_agent(verbose)
        self.verbose = verbose
    
    def invoke(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        调用 Agent
        
        Args:
            message: 用户输入
            session_id: 会话 ID
        
        Returns:
            包含输出的字典
        """
        history = get_session_history(session_id)
        
        # 构建带历史的消息
        messages = []
        for msg in history.messages:
            messages.append(msg)
        
        # 调用 Agent
        result = self.executor.invoke({
            "input": message,
            "history": messages,
        })
        
        # 保存历史
        from langchain_core.messages import HumanMessage, AIMessage
        history.add_message(HumanMessage(content=message))
        history.add_message(AIMessage(content=result.get("output", "")))
        
        return result


# 全局 Agent 实例
_agent_chain: Optional[AgentChain] = None


def get_agent_chain(verbose: bool = False) -> AgentChain:
    """获取或创建全局 Agent 实例"""
    global _agent_chain
    if _agent_chain is None:
        _agent_chain = AgentChain(verbose=verbose)
    return _agent_chain
