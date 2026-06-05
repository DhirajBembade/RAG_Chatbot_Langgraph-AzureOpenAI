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
| `ragas` | Evaluate RAG pipelines — faithfulness, context recall, answer relevancy |
| `deepeval` | CI/CD LLM testing — 50+ metrics, assert-based unit tests for LLM outputs |
| `trulens` | Inline tracing + evaluation — grades every retrieval and generation call |
| `langfuse` | Open-source LLM observability — traces, evals, prompt management |
| `nemoguardrails` | NVIDIA's dialog safety toolkit — jailbreak, prompt injection, hallucination |
| `guardrails-ai` | Composable validators for LLM I/O — PII, toxicity, schema enforcement |
| `azure-ai-contentsafety` | Azure SDK for content moderation — hate, violence, self-harm, sexual |
| `azure-ai-evaluation` | Azure SDK for evaluating LLM outputs — built-in + custom evaluators |

---

## Part 7 — Guardrails

Guardrails are safety layers that **validate, filter, or block** LLM inputs and outputs before they reach users or downstream systems. They protect against:
- Prompt injection / jailbreaks
- Toxic, harmful, or off-topic responses
- PII leakage in outputs
- Hallucinations and factual errors
- Schema violations in structured output

---

### Types of Guardrails

| Type | When Applied | Example |
|---|---|---|
| **Input guardrails** | Before sending to LLM | Block prompt injections, profanity, off-topic queries |
| **Output guardrails** | After LLM responds | Validate JSON schema, detect PII, check factuality |
| **Topical guardrails** | Both | Restrict LLM to specific domains (e.g., only answer HR questions) |
| **Safety guardrails** | Both | Block hate speech, self-harm, violence, CSAM |
| **Structural guardrails** | Output only | Enforce Pydantic model, JSON format, required fields |

---

### 1. Azure Content Safety (Cloud — Azure)

Microsoft's managed API for detecting harmful content across text and images.

```python
pip install azure-ai-contentsafety
```

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,      # Input model for text analysis
    TextCategory,            # Enum: HATE, SELF_HARM, SEXUAL, VIOLENCE
)
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint="https://<resource>.cognitiveservices.azure.com/",
    credential=AzureKeyCredential("<api-key>"),
)

request = AnalyzeTextOptions(text="User message here")
response = client.analyze_text(request)

# Check each category — severity 0-6 (0 = safe, 6 = severe)
for item in response.categories_analysis:
    print(f"{item.category}: severity={item.severity}")
    if item.severity > 2:
        raise ValueError(f"Blocked: {item.category}")
```

| Category | Detects |
|---|---|
| `HATE` | Hate speech, discrimination |
| `SELF_HARM` | Suicide, self-injury content |
| `SEXUAL` | Explicit sexual content |
| `VIOLENCE` | Graphic violence, threats |

---

### 2. AWS Bedrock Guardrails (Cloud — AWS)

Managed guardrails built into Bedrock — applied automatically on every model call.

```python
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Apply guardrail on inference
response = bedrock.invoke_model(
    modelId="anthropic.claude-sonnet-4-6-20251022-v1:0",
    guardrailIdentifier="<guardrail-id>",   # Created in Bedrock console
    guardrailVersion="DRAFT",
    body=json.dumps({
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 1024,
    }),
)
```

**What Bedrock Guardrails cover:**
- Topic denial (block off-topic queries)
- Content filters (hate, insults, violence, misconduct)
- Word filters (custom blocklists)
- PII detection and redaction (email, phone, SSN, credit card)
- Grounding check (detect hallucinations against a ground truth)
- Contextual grounding (verify answer is grounded in context)

---

### 3. NeMo Guardrails (Open Source — NVIDIA)

Programmable dialog safety toolkit — uses a DSL called **Colang** to define safe conversation flows.

```bash
pip install nemoguardrails
```

```python
from nemoguardrails import RailsConfig, LLMRails

# config.yml defines your rails in Colang
config = RailsConfig.from_path("./guardrails_config/")
rails = LLMRails(config)

# Apply rails on every LLM call
response = await rails.generate_async(
    messages=[{"role": "user", "content": "User message"}]
)
```

**Colang config example (`config.yml`):**
```yaml
models:
  - type: main
    engine: openai
    model: gpt-4o

rails:
  input:
    flows:
      - self check input       # Block prompt injections
  output:
    flows:
      - self check output      # Block harmful responses
```

**What NeMo Guardrails cover:**
- Jailbreak detection
- Prompt injection protection
- Topical rails (stay on topic)
- Fact-checking against knowledge base
- Hallucination detection
- Dialog management via Colang flows

---

### 4. Guardrails AI (Open Source)

Composable validator framework — define validators for LLM I/O using pre-built or custom validators from Guardrails Hub.

```bash
pip install guardrails-ai
guardrails hub install hub://guardrails/toxic_language
guardrails hub install hub://guardrails/detect_pii
```

```python
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectPII

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, on_fail="exception"),
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="fix"),
)

# Validate LLM output
validated_output = guard.validate(llm_output)
```

**on_fail options:**
| Option | Behaviour |
|---|---|
| `"exception"` | Raise `ValidationError` — block the response |
| `"fix"` | Auto-fix the output (e.g., redact PII) |
| `"filter"` | Remove the violating part |
| `"reask"` | Re-prompt the LLM to fix its output |
| `"noop"` | Log the violation but pass through |

---

### 5. Llama Guard (Open Source — Meta)

A fine-tuned LLaMA model that classifies inputs/outputs as **safe or unsafe** across 14 harm categories.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Run Llama Guard locally
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-Guard-3-8B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-Guard-3-8B")

# Returns "safe" or "unsafe\nS1" (with category code)
```

**Use case:** Free, self-hosted safety classifier — good for private/on-prem deployments where you can't send data to Azure or AWS.

---

### 6. Pydantic Output Guardrails (Structural)

Force the LLM to always return structured, validated output.

```python
from pydantic import BaseModel, Field, validator
from langchain_core.output_parsers import PydanticOutputParser

class ChatResponse(BaseModel):
    answer: str = Field(description="The answer to the question")
    sources: list[str] = Field(description="List of source document names")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")

    @validator("confidence")
    def confidence_range(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        return v

parser = PydanticOutputParser(pydantic_object=ChatResponse)
chain = prompt | llm | parser  # LLM is forced into this schema
```

---

## Part 8 — Evaluation Metrics

Evaluation tells you **how good your RAG pipeline actually is** — not just "does it run" but "does it answer correctly, relevantly, and faithfully."

---

### RAG Evaluation Dimensions

```
RAG Quality = Retrieval Quality × Generation Quality

Retrieval Quality:
  - Did I retrieve the RIGHT documents? (Context Precision)
  - Did I retrieve ALL the relevant documents? (Context Recall)

Generation Quality:
  - Is the answer grounded in the retrieved docs? (Faithfulness)
  - Does the answer actually address the question? (Answer Relevancy)
```

---

### Core RAGAS Metrics

```bash
pip install ragas
```

| Metric | Measures | Score Range | Formula Idea |
|---|---|---|---|
| **Faithfulness** | Is the answer factually consistent with retrieved context? | 0 – 1 | Claims in answer ÷ total claims |
| **Answer Relevancy** | Does the answer address the user's question? | 0 – 1 | Semantic similarity of answer to question |
| **Context Precision** | Are the retrieved docs actually relevant (no noise)? | 0 – 1 | Relevant docs ÷ total retrieved docs |
| **Context Recall** | Did retrieval cover all aspects of the ground-truth answer? | 0 – 1 | Ground-truth claims found in context ÷ total |
| **Answer Correctness** | Is the answer factually correct vs. ground truth? | 0 – 1 | Requires reference answer |
| **Answer Similarity** | Semantic similarity between answer and reference | 0 – 1 | Cosine similarity of embeddings |
| **Context Entities Recall** | Did retrieved docs contain the right named entities? | 0 – 1 | Entity overlap |
| **Noise Sensitivity** | Does the model get confused by irrelevant context? | 0 – 1 | Lower is better |

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness,
)
from datasets import Dataset

# Your RAG evaluation dataset
data = {
    "question": ["What is RAG?"],
    "answer": ["RAG stands for Retrieval Augmented Generation..."],
    "contexts": [["RAG is a technique that retrieves documents..."]],
    "ground_truth": ["RAG is Retrieval-Augmented Generation, a method..."],
}

dataset = Dataset.from_dict(data)
result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=llm,
    embeddings=embeddings,
)
print(result)  # {'faithfulness': 0.92, 'answer_relevancy': 0.87, ...}
```

---

### DeepEval — CI/CD LLM Testing

Test your LLM like unit tests — assert-based, runs in pytest, blocks bad deployments.

```bash
pip install deepeval
```

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,          # Same as RAGAS faithfulness
    AnswerRelevancyMetric,       # Answer relevance to question
    ContextualPrecisionMetric,   # Retrieval precision
    ContextualRecallMetric,      # Retrieval recall
    HallucinationMetric,         # Detect hallucinations
    ToxicityMetric,              # Detect toxic outputs
    BiasMetric,                  # Detect biased outputs
    GEval,                       # Custom metric defined in natural language
)

test_case = LLMTestCase(
    input="What is RAG?",
    actual_output="RAG stands for Retrieval Augmented Generation...",
    expected_output="RAG is Retrieval-Augmented Generation...",
    retrieval_context=["RAG is a technique that retrieves documents..."],
)

# Run in pytest — fails CI if score < threshold
assert_test(test_case, [
    FaithfulnessMetric(threshold=0.8),
    AnswerRelevancyMetric(threshold=0.7),
])
```

---

### TruLens — Inline Tracing + Evaluation

Couples tracing with evaluation — every single LLM call and retrieval is scored in real time.

```bash
pip install trulens trulens-providers-openai
```

```python
from trulens.core import TruSession, Feedback
from trulens.providers.openai import OpenAI as TruOpenAI
from trulens.apps.langchain import TruChain

session = TruSession()
provider = TruOpenAI()

# Define feedback functions (evaluators)
f_faithfulness = Feedback(provider.groundedness_measure_with_cot_reasons).on_input_output()
f_relevance = Feedback(provider.relevance).on_input_output()

# Wrap your RAG chain
tru_chain = TruChain(
    rag_chain,
    app_name="my-rag-app",
    feedbacks=[f_faithfulness, f_relevance],
)

with tru_chain:
    result = rag_chain.invoke({"question": "What is RAG?"})

session.get_leaderboard()  # View scores across all runs
```

---

### LangSmith — Tracing & Evaluation (LangChain Native)

LangChain's managed observability platform — trace every chain, agent, and LLM call automatically.

```bash
pip install langsmith
```

```bash
# Set environment variables
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your-langsmith-key>
LANGCHAIN_PROJECT=my-rag-project
```

```python
# No code change needed — just set env vars above
# All LangChain / LangGraph calls are automatically traced

# For custom evaluation datasets
from langsmith import Client

client = Client()
dataset = client.create_dataset("rag-eval-dataset")
client.create_examples(
    inputs=[{"question": "What is RAG?"}],
    outputs=[{"answer": "RAG is Retrieval-Augmented Generation..."}],
    dataset_id=dataset.id,
)

# Run evaluation
from langsmith.evaluation import evaluate as ls_evaluate

results = ls_evaluate(
    rag_chain,
    data="rag-eval-dataset",
    evaluators=[faithfulness_evaluator],
)
```

---

### Azure AI Evaluation SDK

Microsoft's official SDK for evaluating LLM outputs on Azure.

```bash
pip install azure-ai-evaluation
```

```python
from azure.ai.evaluation import (
    RelevanceEvaluator,       # Is answer relevant to question?
    CoherenceEvaluator,       # Is answer logically coherent?
    FluencyEvaluator,         # Is answer well-written?
    GroundednessEvaluator,    # Is answer grounded in context?
    SimilarityEvaluator,      # Similarity to ground truth
    F1ScoreEvaluator,         # F1 score vs ground truth
    ViolenceEvaluator,        # Safety: violence detection
    HateUnfairnessEvaluator,  # Safety: hate speech detection
    evaluate,                 # Run batch evaluation
)

model_config = {
    "azure_endpoint": "https://<resource>.openai.azure.com/",
    "api_key": "<key>",
    "azure_deployment": "gpt-4o",
    "api_version": "2024-10-21",
}

relevance_eval = RelevanceEvaluator(model_config=model_config)
groundedness_eval = GroundednessEvaluator(model_config=model_config)

# Single evaluation
score = relevance_eval(
    query="What is RAG?",
    response="RAG stands for Retrieval Augmented Generation...",
)
print(score)  # {'relevance': 4.0}  # 1–5 scale

# Batch evaluation
results = evaluate(
    data="eval_data.jsonl",
    evaluators={
        "relevance": relevance_eval,
        "groundedness": groundedness_eval,
    },
    output_path="./eval_results.json",
)
```

---

### Langfuse — Open-Source Observability

Self-hostable alternative to LangSmith — traces, evals, prompt management, cost tracking.

```bash
pip install langfuse
```

```python
from langfuse.callback import CallbackHandler  # LangChain integration

langfuse_handler = CallbackHandler(
    public_key="<public-key>",
    secret_key="<secret-key>",
    host="https://cloud.langfuse.com",  # or self-hosted URL
)

# Pass as callback to any LangChain / LangGraph call
result = rag_chain.invoke(
    {"question": "What is RAG?"},
    config={"callbacks": [langfuse_handler]},
)
```

---

### Evaluation Metrics Comparison

| Framework | Type | Key Strength | Best For |
|---|---|---|---|
| **RAGAS** | Open source | 4 core RAG metrics, no reference needed | Quick RAG benchmarking |
| **DeepEval** | Open source | 50+ metrics, pytest integration, CI/CD gating | LLM unit testing in pipelines |
| **TruLens** | Open source | Inline tracing + evaluation, production monitoring | Real-time eval in production |
| **LangSmith** | Managed (paid) | Zero-config tracing, dataset management | LangChain/LangGraph teams |
| **Azure AI Evaluation** | Managed (Azure) | Safety + quality evals, Azure-native | Azure production deployments |
| **Langfuse** | Open source + cloud | Self-hostable, cost tracking, prompt versioning | Privacy-sensitive / self-hosted |
| **MLflow** | Open source | Integrates all above, experiment tracking | ML + LLM unified workflow |

---

## Part 9 — Advanced LangChain Retrievers

Beyond basic vector similarity search, LangChain provides advanced retrievers that improve retrieval quality significantly.

---

### MultiQueryRetriever — Generate Multiple Query Variations

Problem: A single embedding query can miss relevant documents due to wording differences.
Solution: Use an LLM to generate 3–5 rephrased versions of the query, retrieve for each, deduplicate.

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm,
)

# Internally generates: "What is RAG?", "Explain retrieval augmented generation",
#                        "How does RAG work?", etc.
docs = retriever.invoke("What is RAG?")
```

---

### ParentDocumentRetriever — Small Chunks, Big Context

Problem: Small chunks = precise search, but loses surrounding context for the LLM.
Solution: Index small chunks for search, but return the full parent document when a chunk matches.

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Small chunks for precise search
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
# Large chunks returned to LLM
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

store = InMemoryStore()  # or RedisStore for production

retriever = ParentDocumentRetriever(
    vectorstore=vector_store,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
retriever.add_documents(docs)
results = retriever.invoke("What is RAG?")  # Returns full parent chunks
```

---

### EnsembleRetriever — Hybrid Search (BM25 + Vector)

Combines keyword search (BM25 — finds exact words) with semantic search (vectors — finds meaning). Best of both worlds.

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(docs)   # Keyword search
bm25_retriever.k = 5

vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})  # Semantic search

# RRF (Reciprocal Rank Fusion) merges and re-ranks results
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6],   # 40% keyword weight, 60% semantic weight
)
docs = ensemble.invoke("What is RAG?")
```

---

### ContextualCompressionRetriever — Filter Irrelevant Content

Retrieves documents then compresses them — only keeps the parts that are actually relevant to the query.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import (
    LLMChainExtractor,    # Use LLM to extract relevant sentences
    EmbeddingsFilter,     # Use embeddings similarity to filter chunks
    DocumentCompressorPipeline,  # Chain multiple compressors
)

compressor = LLMChainExtractor.from_llm(llm)

# or cheaper alternative using embeddings
compressor = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever(search_kwargs={"k": 6}),
)
docs = compression_retriever.invoke("What is RAG?")
# Returns only the relevant sentences, not full chunks
```

---

### SelfQueryRetriever — Natural Language → Metadata Filters

Automatically translates user query into both a semantic search AND metadata filters.

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(name="source", description="PDF filename", type="string"),
    AttributeInfo(name="page", description="Page number", type="integer"),
    AttributeInfo(name="year", description="Publication year", type="integer"),
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vector_store,
    document_contents="Company policy documents",
    metadata_field_info=metadata_field_info,
)

# "Find refund policies from 2024" → filter: year=2024 + search: "refund policy"
docs = retriever.invoke("Find refund policies from 2024")
```

---

### Retriever Quick Reference

| Retriever | Solves | Best For |
|---|---|---|
| `MultiQueryRetriever` | Single query misses relevant docs | General RAG quality boost |
| `ParentDocumentRetriever` | Small chunks lose context | Long documents, precise but contextual |
| `EnsembleRetriever` | Semantic search misses keyword matches | Hybrid search, production RAG |
| `ContextualCompressionRetriever` | Retrieved docs have too much noise | Reducing tokens sent to LLM |
| `SelfQueryRetriever` | User queries need metadata filtering | Structured document collections |

---

## Part 10 — Advanced LangGraph Patterns

---

### Subgraphs — Modular Agents

A compiled graph can be used as a **node** inside another graph. This enables modular, reusable agent components.

```python
from langgraph.graph import StateGraph, START, END

# Sub-agent: handles only retrieval
retrieval_graph = StateGraph(RetrievalState)
retrieval_graph.add_node("embed_query", embed_fn)
retrieval_graph.add_node("search_db", search_fn)
retrieval_graph.add_edge(START, "embed_query")
retrieval_graph.add_edge("embed_query", "search_db")
retrieval_graph.add_edge("search_db", END)
retrieval_subgraph = retrieval_graph.compile()

# Parent graph uses retrieval subgraph as a node
main_graph = StateGraph(MainState)
main_graph.add_node("retrieve", retrieval_subgraph)  # subgraph as node
main_graph.add_node("generate", generate_fn)
main_graph.add_edge(START, "retrieve")
main_graph.add_edge("retrieve", "generate")
main_graph.add_edge("generate", END)
```

---

### Parallel Node Execution

Send control to multiple nodes simultaneously and wait for all to finish before continuing.

```python
from langgraph.graph import StateGraph, START, END

# Both search_web and search_db run in parallel
graph.add_node("search_web", web_search_fn)
graph.add_node("search_db", db_search_fn)
graph.add_node("merge_results", merge_fn)

graph.add_edge(START, "search_web")       # fork
graph.add_edge(START, "search_db")        # fork
graph.add_edge("search_web", "merge_results")   # join
graph.add_edge("search_db", "merge_results")    # join
graph.add_edge("merge_results", END)
```

---

### Streaming LangGraph Output

Stream tokens and state updates to the client in real time.

```python
# Stream LLM tokens
async for chunk in app.astream({"messages": [HumanMessage("Hello")]}, config):
    if chunk.get("generate"):
        print(chunk["generate"]["messages"][-1].content, end="", flush=True)

# Stream all events (node start/end, LLM tokens, tool calls)
async for event in app.astream_events({"messages": [HumanMessage("Hello")]}, config, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="", flush=True)
```

---

### LangGraph Send API — Dynamic Parallel Branches

Dynamically spawn parallel branches at runtime (e.g., process each document in parallel).

```python
from langgraph.types import Send

def dispatch_docs(state):
    # Launch one "process_doc" node per document — all run in parallel
    return [Send("process_doc", {"doc": doc}) for doc in state["documents"]]

graph.add_conditional_edges("load_docs", dispatch_docs)
```

---

## Part 11 — Azure-Specific Components

---

### Azure AI Search — Vector + Hybrid Search

```bash
pip install langchain-community azure-search-documents
```

```python
from langchain_community.vectorstores import AzureSearch
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)

vector_store = AzureSearch(
    azure_search_endpoint="https://<service>.search.windows.net",
    azure_search_key="<admin-key>",
    index_name="my-rag-index",
    embedding_function=embeddings.embed_query,
    search_type="hybrid",   # "similarity" | "hybrid" | "semantic_hybrid"
)

# Hybrid search = vector similarity + BM25 keyword in one query
docs = vector_store.similarity_search("What is RAG?", k=5)
```

---

### Azure AI Document Intelligence

```bash
pip install azure-ai-documentintelligence langchain-community
```

```python
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader

loader = AzureAIDocumentIntelligenceLoader(
    api_endpoint="https://<resource>.cognitiveservices.azure.com/",
    api_key="<key>",
    file_path="./document.pdf",
    api_model="prebuilt-layout",   # Extracts tables, paragraphs, headers
)
docs = loader.load()
```

---

### Azure Key Vault — Secret Management

```bash
pip install azure-keyvault-secrets azure-identity
```

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()  # Uses managed identity in production
client = SecretClient(vault_url="https://<vault>.vault.azure.net/", credential=credential)

api_key = client.get_secret("openai-api-key").value
```

---

### Azure Monitor + OpenTelemetry — LLM Tracing

```bash
pip install azure-monitor-opentelemetry opentelemetry-sdk
```

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(
    connection_string="InstrumentationKey=<key>",
)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("rag-pipeline"):
    result = rag_chain.invoke({"question": "What is RAG?"})
```

---

### Azure Cosmos DB — Chat History at Scale

```bash
pip install langchain-community azure-cosmos
```

```python
from langchain_community.chat_message_histories import CosmosDBChatMessageHistory

history = CosmosDBChatMessageHistory(
    cosmos_endpoint="https://<account>.documents.azure.com:443/",
    cosmos_database="chat_db",
    cosmos_container="sessions",
    session_id="user-123-session-456",
    user_id="user-123",
)
```

---

## Part 12 — Observability & Tracing Quick Reference

| Tool | Type | Key Feature | Setup |
|---|---|---|---|
| **LangSmith** | Managed SaaS | Zero-config LangChain tracing, eval datasets | Set env vars |
| **Langfuse** | OSS + Cloud | Self-hostable, prompt management, cost tracking | `CallbackHandler` |
| **Phoenix (Arize)** | OSS | Local UI, OTEL-native, dataset analysis | `pip install arize-phoenix` |
| **MLflow** | OSS | Unified ML + LLM tracking, integrates RAGAS/DeepEval | `mlflow.langchain.autolog()` |
| **Azure Monitor** | Managed (Azure) | OTEL traces to Application Insights | `configure_azure_monitor()` |
| **W&B Weave** | Managed | Weights & Biases LLM tracing | `weave.init("project")` |

```python
# Enable tracing — pick ONE of these:

# LangSmith (env vars only)
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "<key>"

# Langfuse (callback)
from langfuse.callback import CallbackHandler
handler = CallbackHandler(public_key="...", secret_key="...")
chain.invoke(input, config={"callbacks": [handler]})

# MLflow
import mlflow
mlflow.langchain.autolog()

# Phoenix (local UI at localhost:6006)
import phoenix as px
px.launch_app()
from phoenix.otel import register
register()
```
