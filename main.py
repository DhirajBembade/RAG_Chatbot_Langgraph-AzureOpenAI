from __future__ import annotations

import os
import sqlite3
import tempfile
import uuid
from typing import Annotated, Any, Dict, Optional, TypedDict

import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, tool
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# ---------------------------------------------------------------------------
# 1. LangSmith tracing — controlled via .env
#    Required keys: LANGCHAIN_API_KEY, LANGCHAIN_TRACING_V2=true,
#                   LANGCHAIN_PROJECT (optional, defaults below)
# ---------------------------------------------------------------------------
_LS_ENABLED = os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() == "true"
_LS_PROJECT = os.environ.setdefault("LANGCHAIN_PROJECT", "azure-agentic-rag-chatbot")

# ---------------------------------------------------------------------------
# 2. Azure OpenAI — LLM + Embeddings
#    Required .env keys:
#      AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION,
#      AZURE_OPENAI_DEPLOYMENT  (chat model deployment name)
#      AZURE_OPENAI_EMBEDDING_DEPLOYMENT  (embedding model deployment name)
# ---------------------------------------------------------------------------
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    # temperature=0.5 is not supported by o-series reasoning models (o1/o3/o4-mini);
    # those models only accept the default value of 1.
    streaming=True,
    max_completion_tokens=1000
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# ---------------------------------------------------------------------------
# 3. PDF ingestion — PyMuPDF + FAISS vector store (per thread)
# ---------------------------------------------------------------------------
_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}


def _get_retriever(thread_id: Optional[str]):
    if thread_id and thread_id in _THREAD_RETRIEVERS:
        return _THREAD_RETRIEVERS[thread_id]
    return None


def ingest_pdf(file_bytes: bytes, thread_id: str, filename: Optional[str] = None) -> dict:
    """Build a FAISS retriever from an uploaded PDF via PyMuPDFLoader and cache it per thread."""
    if not file_bytes:
        raise ValueError("No bytes received for ingestion.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name

    try:
        loader = PyMuPDFLoader(temp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(docs)

        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        _THREAD_RETRIEVERS[str(thread_id)] = retriever
        summary = {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }
        _THREAD_METADATA[str(thread_id)] = summary

        # Persist to st.session_state so retrievers survive Streamlit re-runs.
        # Module-level dicts are reset on every re-run; session_state is not.
        st.session_state.setdefault("_thread_retrievers", {})[str(thread_id)] = retriever
        st.session_state.setdefault("_thread_metadata", {})[str(thread_id)] = summary
        return summary
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# 4. Tools
# ---------------------------------------------------------------------------

# -- Web search
duckduckgo_search = DuckDuckGoSearchRun(region="us-en", name="duckduckgo_search")

# -- Wikipedia (wrapped to catch empty/invalid API responses gracefully)
_wikipedia_runner = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=2000),
)


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for encyclopedic facts and background knowledge.

    Args:
        query: The topic or question to look up on Wikipedia
    """
    try:
        return _wikipedia_runner.run(query)
    except Exception as e:
        return f"Wikipedia search failed ({type(e).__name__}: {e}). Try duckduckgo_search instead."


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city. Returns temperature, humidity, wind speed, and conditions.

    Args:
        city: City name (e.g. 'Mumbai', 'London', 'New York')
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()
        current = data["current_condition"][0]
        area = data.get("nearest_area", [{}])[0]
        area_name = area.get("areaName", [{}])[0].get("value", city)
        country = area.get("country", [{}])[0].get("value", "")
        return {
            "city": f"{area_name}, {country}",
            "temperature_c": current.get("temp_C"),
            "temperature_f": current.get("temp_F"),
            "feels_like_c": current.get("FeelsLikeC"),
            "description": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
            "humidity_percent": current.get("humidity"),
            "wind_kmph": current.get("windspeedKmph"),
            "visibility_km": current.get("visibility"),
            "uv_index": current.get("uvIndex"),
        }
    except Exception as e:
        return {"error": f"Could not fetch weather for '{city}': {e}"}


@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch the latest share/stock market price and quote data for a ticker symbol.

    Args:
        symbol: Stock ticker (e.g. 'AAPL', 'TSLA', 'MSFT', 'RELIANCE.BSE')
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    if not api_key:
        return {
            "error": (
                "ALPHA_VANTAGE_API_KEY is not set. "
                "Get a free key at https://www.alphavantage.co/support/#api-key"
            )
        }
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        quote = data.get("Global Quote", {})
        if not quote:
            return {"error": f"No market data found for '{symbol}'. Symbol may be invalid."}
        return {
            "symbol": quote.get("01. symbol"),
            "open": quote.get("02. open"),
            "high": quote.get("03. high"),
            "low": quote.get("04. low"),
            "price": quote.get("05. price"),
            "volume": quote.get("06. volume"),
            "latest_trading_day": quote.get("07. latest trading day"),
            "previous_close": quote.get("08. previous close"),
            "change": quote.get("09. change"),
            "change_percent": quote.get("10. change percent"),
        }
    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}


@tool
def rag_search(query: str, config: Annotated[RunnableConfig, InjectedToolArg]) -> dict:
    """Search the PDF document uploaded in this chat session for relevant passages.

    Args:
        query: The question or topic to search within the document
    """
    thread_id = (config or {}).get("configurable", {}).get("thread_id")
    retriever = _get_retriever(thread_id)
    if retriever is None:
        return {
            "error": "No document indexed for this session. Please upload a PDF first.",
            "query": query,
        }
    docs = retriever.invoke(query)
    return {
        "query": query,
        "source_file": _THREAD_METADATA.get(str(thread_id), {}).get("filename"),
        "context": [doc.page_content for doc in docs],
        "metadata": [doc.metadata for doc in docs],
    }


TOOLS = [duckduckgo_search, wikipedia_search, get_weather, get_stock_price, rag_search]
llm_with_tools = llm.bind_tools(TOOLS)

# ---------------------------------------------------------------------------
# 5. LangGraph state & nodes
# ---------------------------------------------------------------------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are an intelligent agentic assistant powered by Azure OpenAI with five tools:\n"
        "• `rag_search`        — search the user's uploaded PDF document\n"
        "• `duckduckgo_search` — search the web for current news and information\n"
        "• `wikipedia_search`  — look up encyclopedic facts from Wikipedia\n"
        "• `get_weather`       — fetch current weather for any city worldwide\n"
        "• `get_stock_price`   — get live share/stock market prices by ticker symbol\n\n"
        "Guidelines:\n"
        "- When the user asks about an uploaded document, ALWAYS use `rag_search`.\n"
        "- For current events or news, prefer `duckduckgo_search`.\n"
        "- For factual background knowledge, use `wikipedia_search`.\n"
        "- For weather queries, use `get_weather` with the city name.\n"
        "- For stocks/share market queries, use `get_stock_price` with the ticker symbol.\n"
        "- You may call multiple tools in a single turn when needed.\n"
        "- Always give clear, concise, well-structured answers."
    )
)


def _sanitize_messages(messages: list[BaseMessage]) -> list[BaseMessage]:
    """Drop incomplete AIMessage+ToolMessage blocks to avoid Azure OpenAI 400 errors."""
    result: list[BaseMessage] = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        if isinstance(msg, AIMessage) and msg.tool_calls:
            expected_ids = {tc["id"] for tc in msg.tool_calls}
            j = i + 1
            found: dict[str, ToolMessage] = {}
            while j < len(messages) and isinstance(messages[j], ToolMessage):
                found[messages[j].tool_call_id] = messages[j]
                j += 1
            if expected_ids <= found.keys():
                result.append(msg)
                result.extend(found[tid] for tid in expected_ids)
            i = j
        elif isinstance(msg, ToolMessage):
            i += 1
        else:
            result.append(msg)
            i += 1
    return result


def chat_node(state: ChatState, config=None):
    clean = _sanitize_messages(list(state["messages"]))
    response = llm_with_tools.invoke([SYSTEM_PROMPT, *clean], config=config)
    return {"messages": [response]}


tool_node = ToolNode(
    TOOLS,
    handle_tool_errors=lambda e: f"Tool error ({type(e).__name__}): {e}",
)

# ---------------------------------------------------------------------------
# 6. SQLite checkpointer — azure_chatbot.db
# ---------------------------------------------------------------------------
_db_conn = sqlite3.connect(database="azure_chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=_db_conn)

# ---------------------------------------------------------------------------
# 7. Graph
# ---------------------------------------------------------------------------
_graph = StateGraph(ChatState)
_graph.add_node("chat_node", chat_node)
_graph.add_node("tools", tool_node)
_graph.add_edge(START, "chat_node")
_graph.add_conditional_edges("chat_node", tools_condition)
_graph.add_edge("tools", "chat_node")
chatbot = _graph.compile(checkpointer=checkpointer)

# ---------------------------------------------------------------------------
# 8. Session helpers
# ---------------------------------------------------------------------------

def retrieve_all_threads() -> list[str]:
    seen: set[str] = set()
    threads: list[str] = []
    for checkpoint in checkpointer.list(None):
        tid = str(checkpoint.config["configurable"]["thread_id"])
        if tid not in seen:
            seen.add(tid)
            threads.append(tid)
    return threads


def load_thread_conversation(thread_id: str) -> list[dict]:
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    result = []
    for msg in state.values.get("messages", []):
        if isinstance(msg, HumanMessage) and msg.content:
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage) and msg.content:
            result.append({"role": "assistant", "content": msg.content})
    return result


# Old sidebar label — showed only the first 8 chars of the UUID, meaningless to users:
#   label = f"💬 {tid[:8]}…"
# New: derive a human-readable title from the first user message in the thread.
def get_thread_title(thread_id: str) -> str:
    """Return the first user message (truncated) as the conversation title."""
    msgs = load_thread_conversation(thread_id)
    for msg in msgs:
        if msg["role"] == "user" and msg["content"].strip():
            title = msg["content"].strip().replace("\n", " ")
            return title[:45] + "…" if len(title) > 45 else title
    return f"New chat {thread_id[:6]}…"


# ---------------------------------------------------------------------------
# 9. Architecture diagram
# ---------------------------------------------------------------------------

def _draw_architecture_tab():
    """Render the LangGraph topology and full system architecture diagram."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    st.markdown("### How It Works")
    col_l, col_r = st.columns([1, 1])

    # ── Left: LangGraph native Mermaid diagram ────────────────────────────
    with col_l:
        st.markdown("#### LangGraph State Machine")
        try:
            from langgraph.graph.graph import MermaidDrawMethod
            img_bytes = chatbot.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API
            )
            st.image(img_bytes, use_container_width=True)
        except Exception:
            st.code(chatbot.get_graph().draw_mermaid())
            st.caption("Paste into [mermaid.live](https://mermaid.live) to render")

    # ── Right: custom matplotlib system diagram ───────────────────────────
    with col_r:
        st.markdown("#### Full System Flow")

        def _build_fig():
            fig, ax = plt.subplots(figsize=(6, 10))
            ax.set_xlim(0, 6)
            ax.set_ylim(0, 10)
            ax.axis("off")
            fig.patch.set_facecolor("#F8FAFC")

            def rbox(cx, cy, w, h, txt, fc, ec="#444", fs=8):
                ax.add_patch(FancyBboxPatch(
                    (cx - w / 2, cy - h / 2), w, h,
                    boxstyle="round,pad=0.1", fc=fc, ec=ec, lw=1.5, zorder=3,
                ))
                ax.text(cx, cy, txt, ha="center", va="center",
                        fontsize=fs, fontweight="bold", zorder=4,
                        multialignment="center")

            def arr(x1, y1, x2, y2, txt="", clr="#555", rad=0.0):
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(
                                arrowstyle="->", color=clr, lw=1.4,
                                connectionstyle=f"arc3,rad={rad}",
                            ), zorder=2)
                if txt:
                    ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2,
                            txt, fontsize=6.5, color=clr)

            ax.text(3, 9.7, "System Architecture",
                    ha="center", fontsize=9, fontweight="bold", color="#1B2631")

            # User / Streamlit
            rbox(3, 9.2, 5.5, 0.6, "👤  User  /  Streamlit UI",
                 "#AED6F1", "#2E86C1", fs=8.5)

            arr(3, 8.9, 3, 8.45, "chat msg")

            # START node
            ax.plot(3, 8.3, "o", color="#27AE60", ms=13, zorder=4)
            ax.text(3, 8.3, "S", ha="center", va="center",
                    fontsize=7, color="white", fontweight="bold", zorder=5)
            ax.text(3.5, 8.3, "__start__", fontsize=7, va="center", color="#27AE60")

            arr(3, 8.05, 3, 7.55)

            # chat_node
            rbox(3, 7.25, 5.5, 0.6,
                 "🧠  chat_node  ·  Azure OpenAI LLM (5 tools)",
                 "#F9E79F", "#D4AC0D", fs=8)

            ax.text(3, 6.85, "▼  tools_condition",
                    ha="center", fontsize=7, color="#7D6608")

            # YES → ToolNode
            arr(5.0, 7.25, 5.0, 6.3, "tool_calls", "#C0392B")
            rbox(4.6, 6.0, 2.2, 0.55, "🔧  ToolNode", "#FADBD8", "#C0392B", fs=8)

            # Loop back: ToolNode → chat_node
            arr(4.6, 6.27, 3.0, 6.95, "tool results", "#8E44AD", rad=0.4)

            # NO → END
            arr(1.0, 6.95, 1.0, 6.3, "no tools", "#27AE60")
            ax.plot(1.0, 6.05, "o", color="#E74C3C", ms=13, zorder=4)
            ax.text(1.0, 6.05, "E", ha="center", va="center",
                    fontsize=7, color="white", fontweight="bold", zorder=5)
            ax.text(1.5, 6.05, "__end__", fontsize=7, va="center", color="#E74C3C")

            arr(1.0, 5.82, 1.0, 5.35, "stream", "#27AE60")

            # Streamed response box
            rbox(3, 5.1, 5.5, 0.5, "💬  Streamed Response  (st.write_stream)",
                 "#D5F5E3", "#1E8449", fs=8)
            arr(1.5, 5.1, 1.9, 5.1, clr="#27AE60")

            # Tools row
            ax.text(3, 4.65, "── Tools ──",
                    ha="center", fontsize=7.5, color="#555", style="italic")
            tools = ["📄\nrag", "🌐\nddg", "📖\nwiki", "🌤\nwx", "📈\nstock"]
            tfc = ["#D6EAF8", "#D5F5E3", "#FEF9E7", "#EAF2FF", "#F9EBEA"]
            tec = ["#2980B9", "#1E8449", "#B7950B", "#2874A6", "#943126"]
            txs = [0.5, 1.5, 3.0, 4.5, 5.5]
            for lbl, fc, ec, tx in zip(tools, tfc, tec, txs):
                arr(4.6, 5.72, tx, 4.15, clr=ec)
                rbox(tx, 3.9, 0.9, 0.45, lbl, fc, ec, fs=6.5)

            # External services row
            ax.text(3, 3.45, "── External Services ──",
                    ha="center", fontsize=7.5, color="#555", style="italic")
            svcs = ["FAISS\nDB", "DDG\nWeb", "Wiki\nAPI", "wttr\n.in", "Alpha\nVantage"]
            for lbl, fc, ec, tx in zip(svcs, tfc, tec, txs):
                arr(tx, 3.67, tx, 3.22, clr="#999")
                rbox(tx, 2.97, 0.9, 0.45, lbl, fc, ec, fs=6.0)

            # PDF upload note
            ax.text(0.5, 2.5, "📄 PDF Upload\n→ PyMuPDF\n→ FAISS chunks",
                    ha="center", fontsize=5.5, color="#2980B9",
                    style="italic", va="center")

            # Infrastructure row
            ax.text(3, 1.9, "── Infrastructure ──",
                    ha="center", fontsize=7.5, color="#555", style="italic")
            rbox(1.5, 1.3, 2.5, 0.7, "🗄  SQLite\nCheckpointer",
                 "#EAECEE", "#7F8C8D", fs=7)
            rbox(4.5, 1.3, 2.5, 0.7, "🔍  LangSmith\nTracing",
                 "#E8F8F5", "#1ABC9C", fs=7)

            # Dashed lines: infra connected to graph
            ax.annotate("", xy=(1.5, 4.85), xytext=(1.5, 1.65),
                        arrowprops=dict(arrowstyle="->", color="#AAA", lw=1.0,
                                        connectionstyle="arc3,rad=0.4"), zorder=2)
            ax.annotate("", xy=(4.6, 5.72), xytext=(4.5, 1.65),
                        arrowprops=dict(arrowstyle="->", color="#1ABC9C", lw=1.0,
                                        connectionstyle="arc3,rad=0.35"), zorder=2)

            plt.tight_layout()
            return fig

        fig = _build_fig()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ── Step-by-step explanation ──────────────────────────────────────────
    st.divider()
    st.markdown("""
#### Flow Step-by-Step

1. **User sends a message** → Streamlit calls `chatbot.stream()` with the new `HumanMessage`
2. **`chat_node`** — Azure OpenAI LLM receives the full conversation history + system prompt and decides which (if any) tools to call
3. **`tools_condition`** inspects the LLM output:
   - **Has `tool_calls`** → routes to **`ToolNode`**, which executes all requested tools, then loops back to `chat_node` with results
   - **No `tool_calls`** → routes to **`__end__`**, streaming the final reply back to Streamlit
4. **Tools available:**
   - `rag_search` — searches the uploaded PDF via FAISS vector similarity
   - `duckduckgo_search` — live web search
   - `wikipedia_search` — encyclopedic facts
   - `get_weather` — current weather via wttr.in
   - `get_stock_price` — live quotes via Alpha Vantage
5. **SQLite checkpointer** saves every state transition so conversations persist across restarts
6. **LangSmith** traces every node + tool call for observability and debugging
    """)


# ===========================================================================
# Streamlit UI
# ===========================================================================

st.set_page_config(
    page_title="Azure Agentic RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)

# --- Session state init ---
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()
if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}
if "_thread_retrievers" not in st.session_state:
    st.session_state["_thread_retrievers"] = {}
if "_thread_metadata" not in st.session_state:
    st.session_state["_thread_metadata"] = {}
if "thread_titles" not in st.session_state:
    st.session_state["thread_titles"] = {}

# Restore FAISS retrievers into module-level dicts on every re-run.
# Without this, the retrievers built during PDF upload are lost when the user
# sends a message and Streamlit re-runs the script from the top.
_THREAD_RETRIEVERS.update(st.session_state["_thread_retrievers"])
_THREAD_METADATA.update(st.session_state["_thread_metadata"])

thread_key: str = str(st.session_state["thread_id"])
if thread_key not in st.session_state["chat_threads"]:
    st.session_state["chat_threads"].append(thread_key)

thread_docs: dict = st.session_state["ingested_docs"].setdefault(thread_key, {})
threads: list = st.session_state["chat_threads"][::-1]
selected_thread: Optional[str] = None


def _start_new_chat():
    new_tid = str(uuid.uuid4())
    st.session_state["thread_id"] = new_tid
    st.session_state["message_history"] = []
    if new_tid not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(new_tid)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🤖 Azure RAG Chatbot")
    st.caption("Azure OpenAI · LangGraph · LangSmith")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 New Chat", use_container_width=True):
            _start_new_chat()
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    st.divider()
    st.markdown(f"**Session ID:** `{thread_key[:8]}…`")

    # LangSmith status
    if _LS_ENABLED:
        st.success(f"🔍 LangSmith ON\n\n`{_LS_PROJECT}`")
    else:
        st.warning("🔍 LangSmith OFF\n\nSet `LANGCHAIN_TRACING_V2=true` in .env")

    st.divider()

    # PDF upload section
    st.subheader("📄 PDF Document (PyMuPDF)")
    if thread_docs:
        latest = list(thread_docs.values())[-1]
        st.success(
            f"**{latest['filename']}**  \n"
            f"{latest['chunks']} chunks · {latest['documents']} pages"
        )
    else:
        st.info("Upload a PDF to enable document Q&A via RAG.")

    uploaded_pdf = st.file_uploader(
        "Upload PDF", type=["pdf"], label_visibility="collapsed"
    )
    if uploaded_pdf:
        if uploaded_pdf.name in thread_docs:
            st.info(f"`{uploaded_pdf.name}` already indexed for this session.")
        else:
            with st.status("Indexing PDF with PyMuPDF…", expanded=True) as status_box:
                summary = ingest_pdf(
                    uploaded_pdf.getvalue(),
                    thread_id=thread_key,
                    filename=uploaded_pdf.name,
                )
                thread_docs[uploaded_pdf.name] = summary
                status_box.update(
                    label=f"✅ Indexed — {summary['chunks']} chunks",
                    state="complete",
                    expanded=False,
                )

    st.divider()

    # Tools panel
    st.subheader("🛠 Available Tools")
    for icon, name, desc in [
        ("📄", "rag_search", "Query your uploaded PDF"),
        ("🌐", "duckduckgo_search", "Live web search"),
        ("📖", "wikipedia_search", "Encyclopedic facts"),
        ("🌤️", "get_weather", "Current weather by city"),
        ("📈", "get_stock_price", "Live stock/share prices"),
    ]:
        st.markdown(f"{icon} `{name}` — {desc}")

    st.divider()

    # Past conversations
    st.subheader("🕒 Past Conversations")
    if len(threads) <= 1:
        st.caption("No other conversations yet.")
    else:
        for tid in threads:
            # Old label (just UUID prefix, meaningless):
            # label = f"💬 {tid[:8]}…"
            # New: use cached first-message title; fetch once and cache
            if tid not in st.session_state["thread_titles"]:
                st.session_state["thread_titles"][tid] = get_thread_title(tid)
            label = f"💬 {st.session_state['thread_titles'][tid]}"
            if st.button(label, key=f"thread-btn-{tid}", use_container_width=True):
                selected_thread = tid

# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Main area — Chat + Architecture tabs
# ---------------------------------------------------------------------------
chat_tab, arch_tab = st.tabs(["💬 Chat", "🗺 Architecture"])

with chat_tab:
    st.title("🤖 Agentic RAG Chatbot")
    st.caption(
        "Azure OpenAI · LangGraph · PyMuPDF · SQLite (`azure_chatbot.db`) · "
        "Web Search · Wikipedia · Weather · Stock Market"
    )

    # Display conversation history
    for msg in st.session_state["message_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Ask about your PDF, search the web, get weather, check stocks…"
    )

    if user_input:
        st.session_state["message_history"].append({"role": "user", "content": user_input})
        if thread_key not in st.session_state["thread_titles"]:
            title = user_input.strip().replace("\n", " ")
            st.session_state["thread_titles"][thread_key] = (
                title[:45] + "…" if len(title) > 45 else title
            )
        with st.chat_message("user"):
            st.markdown(user_input)

        run_config = {
            "configurable": {"thread_id": thread_key},
            "metadata": {"thread_id": thread_key},
            "run_name": "azure_rag_chat",
        }

        with st.chat_message("assistant"):
            _ctx: dict[str, Any] = {"status_box": None}

            def _stream_response():
                for chunk, _ in chatbot.stream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=run_config,
                    stream_mode="messages",
                ):
                    if isinstance(chunk, AIMessage) and chunk.tool_calls:
                        names = ", ".join(f"`{tc['name']}`" for tc in chunk.tool_calls)
                        if _ctx["status_box"] is None:
                            _ctx["status_box"] = st.status(
                                f"🔧 Calling {names}…", expanded=True
                            )
                        else:
                            _ctx["status_box"].update(
                                label=f"🔧 Calling {names}…",
                                state="running",
                                expanded=True,
                            )
                    elif isinstance(chunk, ToolMessage):
                        if _ctx["status_box"] is not None:
                            _ctx["status_box"].update(
                                label=f"✅ `{chunk.name}` complete",
                                state="complete",
                                expanded=False,
                            )
                            _ctx["status_box"] = None
                    if isinstance(chunk, AIMessage) and chunk.content:
                        yield chunk.content

            ai_reply = st.write_stream(_stream_response())

            if _ctx["status_box"] is not None:
                _ctx["status_box"].update(label="✅ Done", state="complete", expanded=False)

        if ai_reply:
            st.session_state["message_history"].append(
                {"role": "assistant", "content": ai_reply}
            )

        doc_meta = _THREAD_METADATA.get(thread_key, {})
        if doc_meta:
            st.caption(
                f"Document in context: **{doc_meta['filename']}** — "
                f"{doc_meta['chunks']} chunks, {doc_meta['documents']} pages"
            )

    st.divider()
    st.caption("Built with LangGraph · Azure OpenAI · LangSmith · Streamlit · PyMuPDF")

    # Switch to a selected past thread
    if selected_thread:
        st.session_state["thread_id"] = selected_thread
        st.session_state["message_history"] = load_thread_conversation(selected_thread)
        st.session_state["ingested_docs"].setdefault(selected_thread, {})
        st.rerun()

with arch_tab:
    _draw_architecture_tab()
