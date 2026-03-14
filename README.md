# Weather Search Agent 🤖

一个能查天气和搜索网页的 AI Agent，基于 LangChain + LangGraph 和 Qwen 大模型。

## ✨ 功能

- 🌤️ **天气查询** - 查询全球任意城市的实时天气和预报（Open-Meteo，免费）
- 🔍 **网页搜索** - 使用 DuckDuckGo 搜索互联网信息（免费，无需 API Key）
- 💬 **自然对话** - 支持多轮对话，理解上下文
- 🎨 **Web 界面** - 简洁的聊天界面，无需命令行

## 🏗️ 架构

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   用户输入   │ →  │  Web 界面     │ →  │  FastAPI    │
└─────────────┘    └──────────────┘    └─────────────┘
                                              ↓
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   返回结果   │ ←  │  LLM 决策     │ ←  │  Agent     │
└─────────────┘    └──────────────┘    └─────────────┘
                        ↓
            ┌───────────┴───────────┐
            ↓                       ↓
    ┌───────────────┐       ┌───────────────┐
    │ 天气工具       │       │ 搜索工具       │
    │ (Open-Meteo)  │       │ (DuckDuckGo)  │
    └───────────────┘       └───────────────┘
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.11+
- pip 或 Poetry

### 2. 安装

```bash
# 克隆仓库
git clone https://github.com/billhandsome52/weather-search-agent.git
cd weather-search-agent

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install langchain langchain-openai langchain-community langgraph \
    fastapi uvicorn httpx python-dotenv pydantic pydantic-settings duckduckgo-search
```

### 3. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# - 百炼 API Key: https://dashscope.console.aliyun.com/
# ⚠️ 注意：.env 文件包含敏感信息，切勿提交到 Git！
```

**.env 文件示例**：
```bash
# LLM API Configuration (Bailian/Qwen)
DASHSCOPE_API_KEY=sk-your-api-key-here

# Configuration
DEFAULT_LLM_MODEL=qwen3.5-plus
VERBOSE=true

# Note: Search uses DuckDuckGo (free, no API key needed)
# Note: Weather uses Open-Meteo (free, no API key needed)
```

### 4. 运行

```bash
# 启动 Web 服务
uvicorn app.main:app --host 0.0.0.0 --port 8001

# 访问 http://localhost:8001
```

## 💬 使用示例

### 查天气

```
用户：上海今天天气怎么样？
Agent: 上海今天天气不错！🌤️
- 当前温度：13.6°C，主要晴朗
- 湿度：55%
- 风速：11.6 km/h
- 今日预报：部分多云，气温在 5.6°C ~ 17.8°C 之间
```

### 搜索网页

```
用户：搜索 Python 异步编程教程
Agent: 🔍 搜索结果：'Python 异步编程教程'
1. Python 官方文档 - asyncio
   详细介绍 Python 异步编程的基础概念和用法...
   🔗 https://docs.python.org/3/library/asyncio.html
2. Real Python 教程
   循序渐进的 asyncio 教程，适合初学者...
   🔗 https://realpython.com/async-io-python/
```

### 组合查询

```
用户：北京明天会下雨吗？如果下雨帮我搜索室内活动
Agent: 北京明天有小雨，气温 15-20°C。推荐室内活动：
1. 故宫博物院 - 中国最大的古代文化艺术博物馆...
2. 国家图书馆 - 亚洲规模最大的图书馆...
```

## 📁 项目结构

```
weather-search-agent/
├── app/
│   ├── main.py              # FastAPI 入口 + Web 界面
│   ├── agent/
│   │   ├── __init__.py
│   │   └── builder.py       # LangGraph Agent 构建
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather.py       # 天气查询 (Open-Meteo)
│   │   └── search.py        # 网页搜索 (DuckDuckGo)
│   └── config/
│       ├── __init__.py
│       └── settings.py      # 配置管理
├── tests/
│   ├── __init__.py
│   ├── test_weather.py
│   └── test_search.py
├── .env                     # ⚠️ 敏感！不要提交
├── .env.example             # 模板，可以提交
├── .gitignore               # 忽略 .env 等敏感文件
├── pyproject.toml
└── README.md
```

## 🛠️ 技术栈

| 组件 | 技术 | 费用 |
|------|------|------|
| 语言 | Python 3.11+ | 免费 |
| 框架 | LangChain + LangGraph | 免费 |
| LLM | Qwen (阿里百炼) | 付费 (按量) |
| Web | FastAPI + Uvicorn | 免费 |
| 天气 API | Open-Meteo | 免费 |
| 搜索 API | DuckDuckGo | 免费 |

## 🔒 安全提醒

**⚠️ 重要：保护你的 API Key！**

1. **`.env` 文件包含敏感信息**，已在 `.gitignore` 中忽略
2. **永远不要**将 `.env` 文件提交到 Git
3. **永远不要**在代码中硬编码 API Key
4. 使用 `.env.example` 作为模板，提交时只提交模板

```bash
# ✅ 正确做法
cp .env.example .env
# 编辑 .env 填入你的 Key
# .env 自动被 .gitignore 忽略

# ❌ 错误做法
# 在代码中写死 API Key
# 将 .env 添加到 Git
```

## 🔮 未来扩展

- [ ] 网页内容抓取（读取搜索结果页面）
- [ ] 更多工具（计算器、新闻、股票等）
- [ ] 部署为 Telegram/Discord Bot
- [ ] 用户认证和历史记录
- [ ] 流式输出（打字机效果）
- [ ] 支持更多城市（当前使用预定义坐标）

## 📝 License

MIT

## 👤 Author

xuyun

---

**Happy Coding! 🚀**

> 💡 **提示**：遇到问题？检查 `.env` 配置，确保 API Key 正确。搜索和天气功能无需额外 API Key，开箱即用！
