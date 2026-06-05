# config.py
# Loads environment variables from .env and initialises two shared Azure OpenAI clients:
#   - llm        : the chat model used by the LangGraph agent (streaming, tool-bound)
#   - embeddings : the embedding model used to build the FAISS vector store for RAG
# Both are module-level singletons imported by rag.py, tools.py, and graph.py.

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# Load AZURE_OPENAI_* and optional LANGCHAIN_* vars from .env
load_dotenv()

# LangSmith tracing is opt-in; set LANGCHAIN_TRACING_V2=true in .env to enable
LANGSMITH_ENABLED = os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGSMITH_PROJECT = os.environ.setdefault("LANGCHAIN_PROJECT", "azure-agentic-rag-chatbot")

# Chat model — streaming enabled so tokens flow to st.write_stream in real time.
# temperature is not set: o-series reasoning models only accept the default value (1).
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    streaming=True,
    max_completion_tokens=1000,
)

# Embedding model — used once per PDF upload to build the FAISS index
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
