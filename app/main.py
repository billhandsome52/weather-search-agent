"""
Weather Search Agent - Web 入口
"""

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.agent.builder import invoke_agent, get_agent


# 创建 FastAPI 应用
app = FastAPI(
    title="Weather Search Agent",
    description="一个能查天气和搜索网页的 AI Agent",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求/响应模型
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


# 全局 Agent 状态
agent_ready = False


@app.on_event("startup")
async def startup_event():
    """启动时初始化 Agent"""
    global agent_ready
    try:
        get_agent(verbose=settings.verbose)
        agent_ready = True
        print("✅ Agent 初始化成功")
    except Exception as e:
        print(f"⚠️ Agent 初始化失败：{e}")
        agent_ready = False


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回 Web 界面"""
    return get_html_page()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口"""
    if not agent_ready:
        raise HTTPException(status_code=503, detail="Agent 未初始化，请检查 API Key 配置")
    
    # 生成或使用现有会话 ID
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        result = invoke_agent(request.message, session_id)
        return ChatResponse(
            response=result.get("output", "抱歉，我无法回答这个问题"),
            session_id=session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok" if agent_ready else "unavailable",
        "llm_provider": settings.llm_provider,
    }


def get_html_page() -> str:
    """返回 HTML 页面"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Search Agent 🤖</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 800px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            text-align: center;
        }
        .header h1 { font-size: 24px; margin-bottom: 5px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
        }
        .message.user { flex-direction: row-reverse; }
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }
        .message.bot .avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-right: 10px;
        }
        .message.user .avatar {
            background: #e9ecef;
            margin-left: 10px;
        }
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            line-height: 1.5;
        }
        .message.bot .message-content {
            background: white;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
        }
        .input-form { display: flex; gap: 10px; }
        .input-form input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-form input:focus { border-color: #667eea; }
        .input-form button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .input-form button:hover { transform: translateY(-2px); }
        .input-form button:disabled { opacity: 0.6; cursor: not-allowed; }
        .typing-indicator {
            display: none;
            padding: 12px 18px;
            background: white;
            border-radius: 18px;
            width: fit-content;
        }
        .typing-indicator.show { display: block; }
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out;
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        .welcome-message { text-align: center; padding: 40px 20px; color: #6c757d; }
        .welcome-message h2 { margin-bottom: 10px; color: #495057; }
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
        .suggestion {
            padding: 8px 16px;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .suggestion:hover { background: #667eea; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Weather Search Agent</h1>
            <p>问我天气或搜索任何问题</p>
        </div>
        <div class="chat-container" id="chatContainer">
            <div class="welcome-message" id="welcomeMessage">
                <h2>你好！我是 Bill 👋</h2>
                <p>我可以帮你查天气或搜索网页信息</p>
                <div class="suggestions">
                    <div class="suggestion" onclick="useSuggestion('上海今天天气怎么样？')">🌤️ 上海天气</div>
                    <div class="suggestion" onclick="useSuggestion('北京明天会下雨吗？')">🌧️ 北京天气</div>
                    <div class="suggestion" onclick="useSuggestion('搜索 Python 异步编程教程')">🔍 搜索教程</div>
                    <div class="suggestion" onclick="useSuggestion('新加坡天气如何？如果下雨推荐室内活动')">🌦️ 组合查询</div>
                </div>
            </div>
        </div>
        <div class="input-container">
            <form class="input-form" onsubmit="sendMessage(event)">
                <input type="text" id="messageInput" placeholder="输入消息..." autocomplete="off" required>
                <button type="submit" id="sendBtn">发送</button>
            </form>
        </div>
    </div>
    <script>
        let sessionId = null;
        function useSuggestion(text) {
            document.getElementById('messageInput').value = text;
            sendMessage(new Event('submit'));
        }
        function appendMessage(content, isUser = false) {
            const container = document.getElementById('chatContainer');
            const welcome = document.getElementById('welcomeMessage');
            if (welcome) welcome.style.display = 'none';
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user' : 'bot');
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.textContent = isUser ? '👤' : '🤖';
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(contentDiv);
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
        function showTyping() {
            const container = document.getElementById('chatContainer');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator show';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = '<span></span><span></span><span></span>';
            container.appendChild(typingDiv);
            container.scrollTop = container.scrollHeight;
        }
        function hideTyping() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) indicator.remove();
        }
        async function sendMessage(event) {
            event.preventDefault();
            const input = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');
            const message = input.value.trim();
            if (!message) return;
            appendMessage(message, true);
            input.value = '';
            input.disabled = true;
            sendBtn.disabled = true;
            showTyping();
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message, session_id: sessionId}),
                });
                hideTyping();
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || '请求失败');
                }
                const data = await response.json();
                sessionId = data.session_id;
                appendMessage(data.response);
            } catch (error) {
                hideTyping();
                appendMessage('❌ 错误：' + error.message);
            } finally {
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
            }
        }
    </script>
</body>
</html>'''
