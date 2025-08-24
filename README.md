# Discord AI Bot 🤖

A powerful Discord AI bot built with advanced language models, MCP (Model Context Protocol) servers, and comprehensive tooling support. Created by **indrazm**.

## ✨ Features

### 🧠 AI-Powered Conversations

- **GPT-4.1 Integration**: Leverages OpenAI's latest model for intelligent responses
- **Conversation Memory**: Maintains context across Discord threads and channels
- **Multi-modal Support**: Handles both text and image inputs
- **Casual & Friendly Tone**: Designed for natural, conversational interactions

### 🛠️ Advanced Tooling

- **Web Search**: Real-time web search capabilities for up-to-date information
- **GitHub Integration**: Fetch and analyze GitHub repository content using gitingest
- **Context7 MCP Server**: Access to latest documentation for programming languages and frameworks
- **Multi-language Support**: Responds in Bahasa Indonesia when detected, keeping technical terms in English

### 💬 Discord Features

- **Smart Channel Monitoring**: Auto-replies in monitored channels
- **Thread Management**: Creates organized conversation threads
- **Mention Handling**: Responds when mentioned with `@bot`
- **Image Processing**: Analyzes and responds to image attachments
- **Long Message Support**: Handles responses that exceed Discord's character limits

### 📊 Monitoring & Analytics

- **Langfuse Integration**: Comprehensive conversation tracking and analytics
- **Logfire Support**: Advanced logging and monitoring
- **Database Persistence**: SQLite database for conversation history
- **Error Handling**: Robust error handling and logging

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Discord Bot Token
- OpenAI API Key
- Node.js (for MCP servers)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd discord-ai
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Environment Setup**

   ```bash
   cp .env.example .env
   ```

   Fill in your environment variables:

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   MONITORED_CHANNEL_ID=your_channel_id
   OPENAI_API_KEY=your_openai_api_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret
   LANGFUSE_PUBLIC_KEY=your_langfuse_public
   LANGFUSE_HOST=your_langfuse_host
   ```

4. **Database Setup**

   ```bash
   uv run alembic upgrade head
   ```

5. **Run the Bot**
   ```bash
   make serve
   ```

## 🏗️ Architecture

### Project Structure

```
app/
├── core/
│   └── settings.py          # Configuration management
├── database/
│   ├── connection.py        # Database connection
│   ├── models.py           # SQLModel definitions
│   └── service.py          # Database operations
├── discord/
│   ├── bot.py              # Discord bot setup
│   ├── commands.py         # Bot commands
│   ├── events.py           # Event handlers setup
│   ├── handler.py          # Main event handling logic
│   └── utils.py            # Discord utilities
├── llm/
│   ├── agent.py            # AI agent configuration
│   ├── mcps.py             # MCP server management
│   ├── prompts.py          # System prompts
│   ├── tools/
│   │   └── github.py       # GitHub integration tool
│   └── utils.py            # LLM utilities
└── main.py                 # Application entry point
```

### Key Components

#### 🤖 AI Agent (`app/llm/agent.py`)

- Powered by OpenAI's GPT-4.1
- Integrates with MCP servers for enhanced capabilities
- Supports multi-modal inputs (text + images)
- Maintains conversation context

#### 💾 Database Layer (`app/database/`)

- SQLite database with SQLModel ORM
- Conversation history persistence
- Alembic migrations support
- Efficient conversation retrieval

#### 🔧 MCP Integration (`app/llm/mcps.py`)

- Context7 server for documentation access
- Extensible MCP server management
- Async context management for server lifecycle

## 🎯 Usage

### Bot Commands

- `!ping` - Check bot latency
- `!check_channel` - Verify channel monitoring status

### Interaction Modes

1. **Monitored Channel**: Bot auto-replies to all messages
2. **Mention Mode**: Use `@BotName` to start conversations
3. **Thread Conversations**: Maintains context within threads

### Example Interactions

```
User: @DevscaleAI How do I use React hooks?
Bot: lemme check the latest React docs for you! 🔍

[Bot provides comprehensive React hooks explanation with examples]
```

```
User: Can you analyze this GitHub repo? https://github.com/user/project
Bot: Sure! Let me fetch and analyze that repo for you 📊

[Bot provides detailed repository analysis]
```

## 🔧 Configuration

### Environment Variables

| Variable               | Description                 | Required |
| ---------------------- | --------------------------- | -------- |
| `DISCORD_TOKEN`        | Discord bot token           | ✅       |
| `MONITORED_CHANNEL_ID` | Channel ID for auto-replies | ✅       |
| `OPENAI_API_KEY`       | OpenAI API key              | ✅       |
| `LANGFUSE_SECRET_KEY`  | Langfuse secret key         | ❌       |
| `LANGFUSE_PUBLIC_KEY`  | Langfuse public key         | ❌       |
| `LANGFUSE_HOST`        | Langfuse host URL           | ❌       |
| `DATABASE_PATH`        | SQLite database path        | ❌       |
| `DATABASE_ECHO`        | Enable SQL query logging    | ❌       |

### Bot Permissions

Ensure your Discord bot has these permissions:

- Read Messages
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Embed Links
- Attach Files
- Read Message History
- Use Slash Commands

## 🛠️ Development

### Code Quality

- **Ruff**: Linting and formatting
- **Type Hints**: Full type annotation support
- **Async/Await**: Modern async Python patterns
- **Error Handling**: Comprehensive error management

### Adding New Tools

1. Create a new tool in `app/llm/tools/`
2. Use the `@function_tool` decorator
3. Add the tool to the agent in `app/llm/agent.py`

```python
from agents import function_tool

@function_tool
async def my_custom_tool(param: str) -> str:
    """Tool description for the AI agent"""
    # Tool implementation
    return result
```

### Adding MCP Servers

1. Add server configuration in `app/llm/mcps.py`
2. Include in the `get_all_mcp_servers()` function

```python
def get_my_mcp_server():
    return MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "my-mcp-server@latest"],
        }
    )
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Created by **indrazm**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📞 Support

For support and questions, please create an issue in the repository or contact **indrazm**.

---

_Built with ❤️ using Python, Discord.py, OpenAI, and MCP servers_
