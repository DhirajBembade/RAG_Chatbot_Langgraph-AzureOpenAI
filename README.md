# Azure Agentic RAG Chatbot

A conversational AI chatbot built with **LangGraph**, **LangSmith** and **Azure OpenAI** that can search your uploaded PDF documents, browse the web, look up Wikipedia, fetch weather, and check live stock prices — all from a single Streamlit interface.

## Features

- **RAG (Retrieval-Augmented Generation)** — upload a PDF and ask questions about it; answers are grounded in the document via FAISS vector search
- **Web search** — DuckDuckGo for current news and information
- **Wikipedia** — encyclopedic background knowledge
- **Weather** — live weather for any city worldwide (via wttr.in)
- **Stock prices** — real-time quotes via Alpha Vantage
- **Persistent memory** — conversations saved in SQLite (`azure_chatbot.db`) and restored across restarts
- **LangSmith tracing** — optional observability for every node and tool call
- **Streaming responses** — token-by-token output with live tool status indicators

## Project Structure

```
.
├── app.py              # Streamlit entry point
├── config.py           # Azure OpenAI LLM + embeddings setup
├── rag.py              # PDF ingestion and FAISS retriever management
├── tools.py            # Tool definitions (search, weather, stock, RAG)
├── graph.py            # LangGraph state machine and SQLite checkpointer
├── session.py          # Thread/conversation helpers
├── diagrams.py         # Architecture diagram renderer
├── requirements.txt
├── pyproject.toml
└── .env                # Your secrets (never commit this)
```

## Prerequisites

- Python 3.10+
- An Azure OpenAI resource with a **chat** deployment (e.g. `gpt-5.1`) and an **embeddings** deployment (e.g. `text-embedding-3-small`)
- (Optional) A free [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key) for stock prices
- (Optional) A [LangSmith API key](https://smith.langchain.com/) for tracing

## Environment Variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=your-chat-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment-name

# Optional — stock prices
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key

# Optional — LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=azure-agentic-rag-chatbot
```

## Setup

### Using `uv` (recommended)

**macOS / Linux**
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Windows (Command Prompt)**
```cmd
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

### Using standard `venv`

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (Command Prompt)**
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

## How It Works

```
User message
    │
    ▼
chat_node (Azure OpenAI LLM)
    │
    ├── tool_calls? ──► ToolNode ──► (loop back to chat_node)
    │
    └── no tools ──► stream reply to user
```

1. The user sends a message — Streamlit passes it to `chatbot.stream()` as a `HumanMessage`
2. `chat_node` sends the full conversation (+ system prompt) to Azure OpenAI and gets back a response
3. If the LLM decides to use a tool, `ToolNode` executes it and feeds the result back — this loop continues until no more tools are needed
4. The final text reply is streamed token-by-token to the chat window
5. Every state transition is checkpointed to SQLite so you can reload any past conversation from the sidebar

## Tools

| Tool | Description |
|------|-------------|
| `rag_search` | Searches the uploaded PDF using FAISS vector similarity |
| `duckduckgo_search` | Live web search |
| `wikipedia_search` | Encyclopedic facts from Wikipedia |
| `get_weather` | Current weather for any city (wttr.in) |
| `get_stock_price` | Live stock quotes (Alpha Vantage) |
