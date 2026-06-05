# AI Frameworks, RAG Patterns & Production Import Reference

> Interview-ready reference. Covers concepts, components, and every key import with explanation.

---

## Part 1 — Core Concepts

---

### What is LangChain?

LangChain is an **open-source framework** for building applications powered by LLMs. It provides standardized building blocks — loaders, splitters, embeddings, vector stores, chains, agents — so you don't wire everything from scratch.

**Key idea:** Everything is a `Runnable`. You compose runnables into pipelines using the `|` pipe operator (LCEL — LangChain Expression Language).

```python
chain = prompt | llm | output_parser
result = chain.invoke({"question": "What is RAG?"})
```

---

### What is LangGraph?

LangGraph is a **graph-based orchestration framework** built on top of LangChain for building **stateful, multi-step agents and workflows**.

**Key idea:** Your application is modeled as a directed graph — nodes are functions/agents, edges are transitions (conditional or fixed). State flows through the graph and persists across turns via checkpointers.

```
[START] → [retrieve] → [grade_docs] → [generate] → [END]
                              ↓ (bad docs)
                          [rewrite_query] → [retrieve]
```

**LangChain vs LangGraph:**
| | LangChain | LangGraph |
|---|---|---|
| Model | Linear chains / pipelines | Cyclic graphs with state |
| Memory | Stateless by default | Built-in persistent state |
| Loops | Not supported | Native cycles and loops |
| Best for | Simple RAG, one-shot chains | Agents, multi-step workflows |

---

### What is RAG?

**RAG (Retrieval-Augmented Generation)** is a pattern where you:
1. **Retrieve** relevant documents from a knowledge base (vector DB)
2. **Augment** the LLM prompt with those documents
3. **Generate** an answer grounded in the retrieved content

Without RAG, the LLM answers only from training data (may be outdated or hallucinate). With RAG, it answers from *your* data.

```
User: "What is our refund policy?"
         ↓
[Embed question] → [Search vector DB] → [Top-3 policy docs]
         ↓
[LLM: "Based on the docs: refunds within 30 days..."]
```

**RAG Pipeline Steps:**
```
INDEXING (offline):
  PDF / Web / DB  →  Loader  →  Splitter  →  Embeddings  →  Vector DB

RETRIEVAL (online):
  User Query  →  Embed  →  Vector Search  →  Top-K Chunks  →  LLM  →  Answer
```

---

### What is Multi-RAG?

**Multi-RAG** (also called Multi-Source RAG or Federated RAG) retrieves from **multiple knowledge sources simultaneously** and merges or re-ranks the results before passing to the LLM.

**Use cases:**
- Querying both a PDF store and a SQL database at once
- Searching across multiple domain-specific vector collections
- Combining internal docs + web search results

```
User Query
    ├── → Vector DB (PDFs)        ┐
    ├── → SQL Database            ├── Merge + Re-rank → LLM → Answer
    └── → Web Search (Tavily)     ┘
```

**Key difference from basic RAG:** Multiple retrieval paths, result fusion/ranking before generation.

---

### What is Agentic RAG?

**Agentic RAG** combines a RAG pipeline with an **autonomous agent** that can decide *when* and *how* to retrieve, can re-query, can route between tools, and can verify its own answers.

The agent is not just a retriever — it reasons, reflects, and acts in a loop.

**Patterns in Agentic RAG:**
| Pattern | Meaning |
|---|---|
| **Self-RAG** | Agent grades its own retrieved docs and rewrites the query if they're not relevant |
| **Corrective RAG (CRAG)** | Checks retrieved docs, falls back to web search if confidence is low |
| **Adaptive RAG** | Routes query to simple RAG, complex RAG, or direct LLM based on query type |
| **RAG Fusion** | Generates multiple sub-queries, retrieves for each, fuses results |

```
[User Query]
     ↓
[Agent decides: simple RAG or web search?]
     ↓
[Retrieves] → [Grades relevance] → [Good? Generate] → [Answer]
                    ↓ (not good)
             [Rewrite query] → [Retrieve again]
```

---

## Part 2 — LangChain Components

| Component | What It Does |
|---|---|
| **Document Loaders** | Load raw data from PDF, web, DB, S3, etc. into `Document` objects |
| **Text Splitters** | Split large documents into smaller chunks for embedding |
| **Embedding Models** | Convert text chunks into vectors |
| **Vector Stores** | Store and search vectors (Chroma, Qdrant, FAISS, pgvector) |
| **Retrievers** | Interface that returns relevant documents given a query |
| **Prompts** | Templates for structuring LLM inputs |
| **LLMs / Chat Models** | The AI model that generates responses |
| **Output Parsers** | Parse LLM output into structured formats (str, JSON, Pydantic) |
| **Chains (LCEL)** | Composable pipelines: `prompt | llm | parser` |
| **Memory** | Store and retrieve conversation history |
| **Tools** | Functions the LLM can call (search, calculator, DB query) |
| **Agents** | LLM + tools in a reasoning loop (ReAct, OpenAI Functions) |
| **Callbacks** | Hooks for logging, tracing, streaming |

---

## Part 3 — LangGraph Components

| Component | What It Does |
|---|---|
| **StateGraph** | The main graph class — defines nodes, edges, and state schema |
| **State** | A typed dict or Pydantic model that flows through the graph and is updated at each node |
| **Nodes** | Python functions that receive state, do work, return updated state |
| **Edges** | Connections between nodes (fixed or conditional) |
| **START / END** | Built-in sentinel nodes — entry and exit points of the graph |
| **Conditional Edges** | Route to different nodes based on state (e.g., if doc is relevant → generate, else → rewrite) |
| **ToolNode** | Pre-built node that executes a list of tools based on LLM tool calls |
| **tools_condition** | Pre-built conditional edge — routes to ToolNode if tool calls exist, else END |
| **MemorySaver** | In-memory checkpointer — persists state between invocations (dev/testing) |
| **SqliteSaver** | SQLite-backed checkpointer — lightweight persistence (local/POC) |
| **PostgresSaver** | Postgres-backed checkpointer — production-grade persistence |
| **create_react_agent** | Pre-built ReAct agent — LLM + tools loop in one line |
| **interrupt** | Pause graph execution and wait for human input (human-in-the-loop) |
| **Command** | Return value from a node that both updates state AND controls routing |
| **Subgraph** | A compiled graph used as a node inside another graph (modular agents) |

---

## Part 4 — All Key Imports with Explanations

---

### LangChain Core — Messages

```python
from langchain_core.messages import (
    BaseMessage,      # Abstract base class for all message types
    HumanMessage,     # Message from the user
    AIMessage,        # Message from the AI / LLM
    SystemMessage,    # System-level instruction (sets LLM behavior)
    ToolMessage,      # Result returned from a tool call
    FunctionMessage,  # Legacy — prefer ToolMessage
)
```

| Class | When You Use It |
|---|---|
| `BaseMessage` | Type hint for functions that accept any message type |
| `HumanMessage` | Wrap user input before passing to LLM |
| `AIMessage` | Wrap LLM response when building conversation history |
| `SystemMessage` | Set persona / instructions at the start of a conversation |
| `ToolMessage` | Return tool execution result back to the LLM |

---

### LangChain Core — Prompts

```python
from langchain_core.prompts import (
    ChatPromptTemplate,      # Build structured chat prompts with placeholders
    MessagesPlaceholder,     # Insert a list of messages (history) into a prompt
    PromptTemplate,          # Simple string prompt with {variables}
    HumanMessagePromptTemplate,  # Human turn template
    SystemMessagePromptTemplate, # System turn template
)
```

| Class | When You Use It |
|---|---|
| `ChatPromptTemplate` | Most common — builds prompt with system + human + history turns |
| `MessagesPlaceholder` | Inject full conversation history into chat prompt |
| `PromptTemplate` | Simple non-chat prompts, summarization, extraction |

---

### LangChain Core — Output Parsers

```python
from langchain_core.output_parsers import (
    StrOutputParser,      # Convert LLM output to plain string
    JsonOutputParser,     # Parse LLM output as JSON dict
    PydanticOutputParser, # Parse LLM output into a Pydantic model
    ListOutputParser,     # Parse output as Python list
)
```

---

### LangChain Core — Runnables (LCEL)

```python
from langchain_core.runnables import (
    RunnablePassthrough,   # Pass input unchanged — used in RAG to forward the question
    RunnableLambda,        # Wrap any Python function as a Runnable
    RunnableParallel,      # Run multiple runnables in parallel, merge outputs
    RunnableSequence,      # Chain runnables sequentially (equivalent to pipe |)
    RunnableWithMessageHistory,  # Wrap a chain to auto-manage chat history
)
```

**RAG chain example using LCEL:**
```python
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

---

### LangChain Core — Documents & Retrievers

```python
from langchain_core.documents import Document          # Holds page_content + metadata
from langchain_core.vectorstores import VectorStore    # Base class for all vector stores
from langchain_core.embeddings import Embeddings       # Base class for embedding models
from langchain_core.retrievers import BaseRetriever    # Base class for all retrievers
```

---

### LangChain Core — Tools

```python
from langchain_core.tools import (
    tool,         # @tool decorator — turn any function into a LangChain tool
    BaseTool,     # Base class for custom tools with schema validation
    StructuredTool,  # Tool with input schema defined via Pydantic
)
```

---

### LangChain OpenAI / Azure (langchain_openai)

```python
from langchain_openai import (
    AzureChatOpenAI,        # Chat LLM via Azure OpenAI (GPT-4o, GPT-5.4, etc.)
    ChatOpenAI,             # Chat LLM via OpenAI direct API
    AzureOpenAIEmbeddings,  # Embeddings via Azure OpenAI (text-embedding-3-small)
    OpenAIEmbeddings,       # Embeddings via OpenAI direct API
)
```

**AzureChatOpenAI — production setup:**
```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",          # Your deployment name in Azure portal
    azure_endpoint="https://<resource>.openai.azure.com/",
    api_key="<your-api-key>",           # or use env var AZURE_OPENAI_API_KEY
    api_version="2024-10-21",           # Use latest stable API version
    temperature=0,                      # 0 = deterministic, 1 = creative
    max_tokens=4096,
    streaming=True,                     # Enable for real-time token streaming
)
```

**AzureOpenAIEmbeddings:**
```python
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-small",
    azure_endpoint="https://<resource>.openai.azure.com/",
    api_key="<your-api-key>",
    api_version="2024-10-21",
)
```

---

### LangChain Community — Document Loaders

```python
from langchain_community.document_loaders import (
    PyPDFLoader,              # Load PDF using pypdf — text only, no OCR
    UnstructuredPDFLoader,    # Load PDF using Unstructured — handles complex layouts
    TextLoader,               # Load plain .txt files
    WebBaseLoader,            # Scrape and load a webpage
    DirectoryLoader,          # Load all files from a folder
    CSVLoader,                # Load CSV as documents (one row = one doc)
    JSONLoader,               # Load JSON with jq-path extraction
    AzureBlobStorageFileLoader,  # Load file directly from Azure Blob Storage
    S3FileLoader,             # Load file directly from AWS S3
    UnstructuredWordDocumentLoader,  # Load .docx files
)
```

| Loader | When to Use |
|---|---|
| `PyPDFLoader` | Clean PDFs with embedded text — fast, no OCR |
| `UnstructuredPDFLoader` | Complex PDFs with tables, columns, mixed layouts |
| `WebBaseLoader` | Load webpage content for RAG |
| `DirectoryLoader` | Bulk-ingest a folder of files |
| `AzureBlobStorageFileLoader` | Load docs directly from Azure Blob — no local download |

---

### LangChain Community — Vector Stores

```python
from langchain_community.vectorstores import (
    FAISS,      # In-memory, fast — dev / prototyping, no persistence
    Chroma,     # Local persistent vector DB — great for POC
)

from langchain_chroma import Chroma             # Newer dedicated package (prefer this)
from langchain_qdrant import QdrantVectorStore  # Qdrant — production self-hosted / cloud
from langchain_pinecone import PineconeVectorStore  # Pinecone — fully managed cloud
from langchain_community.vectorstores import AzureSearch  # Azure AI Search
```

---

### LangChain — Text Splitters

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,  # Best default — splits by paragraph, sentence, word
    CharacterTextSplitter,           # Splits by a single separator (e.g. "\n\n")
    TokenTextSplitter,               # Splits by token count — use with specific LLM limits
    MarkdownHeaderTextSplitter,      # Splits Markdown by headers (H1, H2, H3)
    HTMLHeaderTextSplitter,          # Splits HTML by heading tags
)
```

**Most used — RecursiveCharacterTextSplitter:**
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Max characters per chunk
    chunk_overlap=200,     # Overlap between chunks to preserve context
    separators=["\n\n", "\n", " ", ""],  # Try these in order
)
docs = splitter.split_documents(raw_docs)
```

---

### LangChain — HuggingFace (local embeddings)

```python
from langchain_huggingface import (
    HuggingFaceEmbeddings,   # Run embedding model locally — free, no API key
    HuggingFacePipeline,     # Run open-source LLM locally via transformers pipeline
    ChatHuggingFace,         # Chat interface for HuggingFace models
)
```

```python
# Free local embeddings — no API cost
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",              # Best open embedding model
    model_kwargs={"device": "cpu"},        # or "cuda" for GPU
    encode_kwargs={"normalize_embeddings": True},
)
```

---

### LangChain — Memory / Chat History

```python
from langchain_community.chat_message_histories import (
    ChatMessageHistory,           # In-memory message history (dev / testing)
    RedisChatMessageHistory,      # Redis-backed history — production, multi-user
    SQLChatMessageHistory,        # SQL-backed history (PostgreSQL, SQLite)
    DynamoDBChatMessageHistory,   # DynamoDB-backed — AWS production
    CosmosDBChatMessageHistory,   # Cosmos DB — Azure production
)

from langchain_core.runnables import RunnableWithMessageHistory  # Wrap chain with history
```

---

### LangChain — Tools (Community)

```python
from langchain_community.tools import (
    DuckDuckGoSearchRun,      # Free web search — no API key needed
    WikipediaQueryRun,        # Query Wikipedia
    TavilySearchResults,      # Tavily search API — best for RAG agents (paid)
    ArxivQueryRun,            # Search ArXiv papers
)

from langchain_community.agent_toolkits import (
    SQLDatabaseToolkit,       # Give agent access to a SQL database
    FileManagementToolkit,    # Give agent access to read/write files
)
```

---

### LangGraph — Graph Building

```python
from langgraph.graph import (
    StateGraph,    # Main class — define your graph with typed state
    MessageGraph,  # Simplified graph where state IS the message list (chat agents)
    START,         # Sentinel — marks the entry edge of the graph
    END,           # Sentinel — marks the terminal node(s) of the graph
)
```

**Basic graph pattern:**
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: list
    context: str
    answer: str

graph = StateGraph(State)
graph.add_node("retrieve", retrieve_fn)
graph.add_node("generate", generate_fn)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()
```

---

### LangGraph — Prebuilt Nodes & Conditions

```python
from langgraph.prebuilt import (
    create_react_agent,   # One-line ReAct agent: LLM + tools loop
    ToolNode,             # Node that executes tool calls from AIMessage
    tools_condition,      # Edge condition: go to ToolNode if tool_calls exist, else END
)
```

**ReAct agent in 3 lines:**
```python
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search the web."""
    return "result..."

agent = create_react_agent(llm, tools=[search])
result = agent.invoke({"messages": [HumanMessage("What is RAG?")]})
```

---

### LangGraph — Checkpointers (Memory / Persistence)

```python
from langgraph.checkpoint.memory import MemorySaver      # In-memory — dev/testing only
from langgraph.checkpoint.sqlite import SqliteSaver      # SQLite — lightweight local persistence
from langgraph.checkpoint.postgres import PostgresSaver  # Postgres — production multi-user
```

```python
# Production pattern
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

conn = psycopg.connect("postgresql://user:pass@host/db")
checkpointer = PostgresSaver(conn)
app = graph.compile(checkpointer=checkpointer)

# Each thread_id = separate conversation with full history
config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"messages": [HumanMessage("Hello")]}, config=config)
```

---

### LangGraph — Human-in-the-Loop

```python
from langgraph.types import (
    interrupt,   # Pause graph, surface question to human, resume with answer
    Command,     # Return from node with both state update AND routing decision
)
```

```python
def human_approval_node(state):
    decision = interrupt("Approve this action? (yes/no)")  # Pauses here
    if decision == "yes":
        return Command(goto="execute", update={"approved": True})
    return Command(goto=END)
```

---

### MCP (Model Context Protocol)

MCP is an open protocol by Anthropic that lets LLMs connect to external tools and data sources via a standardized server/client interface.

```python
# MCP client — connect to an MCP server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain MCP adapter — load MCP tools as LangChain tools
from langchain_mcp_adapters.tools import load_mcp_tools

# LangGraph + MCP agent
from langgraph.prebuilt import create_react_agent
```

**MCP agent pattern:**
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

server_params = StdioServerParameters(
    command="python",
    args=["my_mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await load_mcp_tools(session)   # MCP tools → LangChain tools
        agent = create_react_agent(llm, tools)
        result = await agent.ainvoke({"messages": [HumanMessage("Run the query")]})
```

---

### AWS Bedrock — LangChain Integration

```python
from langchain_aws import (
    ChatBedrock,          # Chat LLM via AWS Bedrock (Claude, Nova, Llama, Mistral)
    BedrockEmbeddings,    # Embeddings via AWS Bedrock (Titan, Cohere)
    BedrockLLM,           # Completion (non-chat) LLM via Bedrock (legacy)
)

import boto3  # AWS SDK — required for auth
```

**ChatBedrock setup:**
```python
from langchain_aws import ChatBedrock
import boto3

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

llm = ChatBedrock(
    model_id="anthropic.claude-sonnet-4-6-20251022-v1:0",
    client=bedrock_client,
    model_kwargs={
        "temperature": 0,
        "max_tokens": 4096,
    },
)
```

**BedrockEmbeddings setup:**
```python
from langchain_aws import BedrockEmbeddings

embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    client=bedrock_client,
)
```

---

### FastAPI — Production API Layer

```python
from fastapi import (
    FastAPI,             # Main app instance
    HTTPException,       # Raise HTTP errors (404, 500, etc.)
    Depends,             # Dependency injection (auth, DB sessions)
    BackgroundTasks,     # Run tasks after returning response
    Request,             # Access raw HTTP request
    status,              # HTTP status code constants
)

from fastapi.middleware.cors import CORSMiddleware   # Allow cross-origin requests (browser)
from fastapi.responses import (
    StreamingResponse,   # Stream LLM tokens to client in real time
    JSONResponse,        # Return JSON response explicitly
)

from pydantic import BaseModel, Field  # Request/response schema validation

import uvicorn  # ASGI server to run FastAPI
```

**Production FastAPI + streaming LLM pattern:**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

@app.post("/chat")
async def chat(req: ChatRequest):
    async def token_stream():
        async for chunk in llm.astream([HumanMessage(req.message)]):
            yield chunk.content

    return StreamingResponse(token_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Part 5 — Complete Import Cheat Sheet

### POC / Local Development

```python
# LLM
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Embeddings (free local)
from langchain_huggingface import HuggingFaceEmbeddings

# Vector DB (local, no server)
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

# Document loading
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, DirectoryLoader

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Prompts
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Chain building
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Graph
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Tools
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
```

---

### Production

```python
# LLM — Azure
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# LLM — AWS Bedrock
from langchain_aws import ChatBedrock, BedrockEmbeddings
import boto3

# Vector DB — production
from langchain_qdrant import QdrantVectorStore
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import AzureSearch  # Azure AI Search

# Document loaders — cloud storage
from langchain_community.document_loaders import (
    AzureBlobStorageFileLoader,
    S3FileLoader,
    UnstructuredPDFLoader,
)

# Memory — persistent
from langchain_community.chat_message_histories import (
    RedisChatMessageHistory,
    SQLChatMessageHistory,
)
from langchain_core.runnables import RunnableWithMessageHistory

# Graph — production
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode, tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import interrupt, Command

# MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

# API
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter

# Output
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser

# Callbacks / Tracing
from langchain_core.callbacks import StreamingStdOutCallbackHandler
```

---

### Packages to Install

```bash
# Core
pip install langchain langchain-core langchain-community langchain-text-splitters

# LLM providers
pip install langchain-openai          # OpenAI + Azure OpenAI
pip install langchain-aws boto3       # AWS Bedrock
pip install langchain-google-vertexai # Google Vertex AI / Gemini

# Vector DBs
pip install langchain-chroma chromadb
pip install langchain-qdrant qdrant-client
pip install langchain-pinecone pinecone-client

# Embeddings (local)
pip install langchain-huggingface sentence-transformers

# Graph
pip install langgraph

# MCP
pip install mcp langchain-mcp-adapters

# PDF / Document loaders
pip install pypdf unstructured pymupdf4llm docling

# API
pip install fastapi uvicorn[standard] pydantic

# Tracing / Observability
pip install langsmith          # LangChain's tracing platform
pip install opentelemetry-sdk  # Open standard tracing
```

---

## Part 6 — Why Each Package Exists (One-Liner)

| Package | Why You Need It |
|---|---|
| `langchain-core` | The base interfaces — messages, runnables, tools, prompts. Install first. |
| `langchain-openai` | Connects LangChain to OpenAI / Azure OpenAI — `AzureChatOpenAI`, embeddings |
| `langchain-aws` | Connects LangChain to AWS Bedrock — `ChatBedrock`, `BedrockEmbeddings` |
| `langchain-community` | 300+ third-party integrations — loaders, vector stores, tools, memory |
| `langchain-text-splitters` | All chunking strategies — `RecursiveCharacterTextSplitter` is the default |
| `langchain-huggingface` | Run free open-source embedding/LLM models locally without API cost |
| `langchain-chroma` | Local vector DB — perfect for POC, no server needed |
| `langchain-qdrant` | Production vector DB — fast, Rust-based, free self-hosted |
| `langgraph` | Build stateful multi-step agents and cyclic workflows on top of LangChain |
| `mcp` | Anthropic's Model Context Protocol — connect LLMs to external tool servers |
| `langchain-mcp-adapters` | Bridge between MCP tools and LangChain/LangGraph |
| `fastapi` | Build REST / streaming API endpoints for your chatbot |
| `uvicorn` | ASGI server to run FastAPI in production |
| `pydantic` | Data validation for request/response schemas and LLM structured output |
| `pypdf` | Extract text from PDFs (used by `PyPDFLoader`) |
| `unstructured` | Advanced PDF/doc parsing with layout understanding and OCR |
| `langsmith` | Trace and debug LangChain/LangGraph runs — essential for production |
| `boto3` | AWS SDK — required for Bedrock authentication and S3 access |
