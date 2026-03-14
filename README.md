# Weather Search Agent 🤖

一个能查天气和搜索网页的 AI Agent，基于 LangChain 和 Qwen 大模型。

## ✨ 功能

- 🌤️ **天气查询** - 查询全球任意城市的实时天气和预报
- 🔍 **网页搜索** - 使用 Brave Search 搜索互联网信息
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
    │ (Open-Meteo)  │       │ (Brave)       │
    └───────────────┘       └───────────────┘
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.11+
- Poetry（包管理）

### 2. 安装

```bash
# 克隆仓库
git clone https://github.com/xuyun/weather-search-agent.git
cd weather-search-agent

# 安装依赖
poetry install
```

### 3. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# - 百炼 API Key: https://dashscope.console.aliyun.com/
# - Brave API Key: https://brave.com/search/api/
```

### 4. 运行

```bash
# 启动 Web 服务
poetry run python app/main.py

# 访问 http://localhost:8000
```

## 💬 使用示例

### 查天气

```
用户：上海今天天气怎么样？
Agent: 上海今天晴，气温 18-25°C，东风 3 级，湿度 65%
```

### 搜索网页

```
用户：帮我搜索 Python 异步编程的最佳实践
Agent: 找到以下结果：
1. Python 官方文档 - asyncio...
2. Real Python 教程...
...
```

### 组合查询

```
用户：北京明天会下雨吗？如果下雨帮我搜索室内活动
Agent: 北京明天有小雨，气温 15-20°C。推荐室内活动：
1. 故宫博物院...
2. 国家图书馆...
```

## 📁 项目结构

```
weather-search-agent/
├── app/
│   ├── main.py              # FastAPI 入口 + Web 界面
│   ├── agent/
│   │   └── builder.py       # Agent 构建逻辑
│   ├── tools/
│   │   ├── weather.py       # 天气查询工具
│   │   └── search.py        # 网页搜索工具
│   └── config/
│       └── settings.py      # 配置管理
├── tests/
│   ├── test_weather.py
│   └── test_search.py
├── pyproject.toml
├── .env.example
└── README.md
```

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.11+ |
| 框架 | LangChain |
| LLM | Qwen (阿里百炼) |
| Web | FastAPI |
| 天气 API | Open-Meteo (免费) |
| 搜索 API | Brave Search |

## 🔮 未来扩展

- [ ] 网页内容抓取（读取搜索结果页面）
- [ ] 更多工具（计算器、新闻、股票等）
- [ ] 部署为 Telegram/Discord Bot
- [ ] 用户认证和历史记录
- [ ] 流式输出（打字机效果）

## 📝 License

MIT

## 👤 Author

xuyun

---

**Happy Coding! 🚀**
