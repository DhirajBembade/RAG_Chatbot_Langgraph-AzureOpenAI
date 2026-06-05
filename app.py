# app.py
# Streamlit entry point — run with: streamlit run app.py
#
# Responsibilities:
#   - Page config and session state initialisation
#   - Sidebar: new-chat button, LangSmith status, PDF uploader, tools panel, past conversations
#   - Chat tab: renders message history, streams LLM responses token-by-token,
#               shows live tool-call status indicators via st.status
#   - Architecture tab: delegates to diagrams.draw_architecture_tab()

from __future__ import annotations

import json
import uuid
from typing import Any, Optional

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from config import LANGSMITH_ENABLED, LANGSMITH_PROJECT
from diagrams import draw_architecture_tab
from graph import chatbot
from rag import get_metadata, ingest_pdf, sync_from_session
from session import get_thread_title, load_thread_conversation, retrieve_all_threads

st.set_page_config(
    page_title="Azure Agentic RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)

# One-time defaults — Streamlit re-runs this file on every interaction,
# so guards prevent overwriting state that already exists
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

# Restore FAISS retrievers into module-level dicts after every Streamlit re-run
sync_from_session()

thread_key: str = str(st.session_state["thread_id"])
if thread_key not in st.session_state["chat_threads"]:
    st.session_state["chat_threads"].append(thread_key)

thread_docs: dict = st.session_state["ingested_docs"].setdefault(thread_key, {})
threads: list = st.session_state["chat_threads"][::-1]
selected_thread: Optional[str] = None


def start_new_chat():
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
            start_new_chat()
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    st.divider()
    st.markdown(f"**Session ID:** `{thread_key[:8]}…`")

    if LANGSMITH_ENABLED:
        st.success(f"🔍 LangSmith ON\n\n`{LANGSMITH_PROJECT}`")
    else:
        st.warning("🔍 LangSmith OFF\n\nSet `LANGCHAIN_TRACING_V2=true` in .env")

    st.divider()

    # PDF upload
    st.subheader("📄 PDF Document")
    if thread_docs:
        latest = list(thread_docs.values())[-1]
        st.success(
            f"**{latest['filename']}**  \n"
            f"{latest['chunks']} chunks · {latest['documents']} pages"
        )
    else:
        st.info("Upload a PDF to enable document Q&A via RAG.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_pdf:
        if uploaded_pdf.name in thread_docs:
            st.info(f"`{uploaded_pdf.name}` already indexed for this session.")
        else:
            with st.status("Indexing PDF…", expanded=True) as status_box:
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
            if tid not in st.session_state["thread_titles"]:
                st.session_state["thread_titles"][tid] = get_thread_title(tid)
            label = f"💬 {st.session_state['thread_titles'][tid]}"
            if st.button(label, key=f"thread-btn-{tid}", use_container_width=True):
                selected_thread = tid


# ---------------------------------------------------------------------------
# Sources panel — renders tool results below each assistant answer
# ---------------------------------------------------------------------------

_TOOL_ICONS = {
    "rag_search": "📄",
    "duckduckgo_search": "🌐",
    "wikipedia_search": "📖",
    "get_weather": "🌤️",
    "get_stock_price": "📈",
}


def _render_sources(tool_results: list[dict]) -> None:
    count = len(tool_results)
    label = f"🔍 Search Results · {count} source{'s' if count > 1 else ''} used"

    with st.expander(label, expanded=True):
        for i, result in enumerate(tool_results):
            icon = _TOOL_ICONS.get(result["tool"], "🔧")
            st.markdown(f"**{icon} `{result['tool']}`**")

            content = result["content"]

            # Tool functions return dicts; ToolMessage serialises them to JSON strings
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except (json.JSONDecodeError, ValueError):
                    pass

            if isinstance(content, dict):
                # RAG: show each retrieved passage as a quoted block
                if "context" in content:
                    src = content.get("source_file", "document")
                    st.caption(f"Source: **{src}**")
                    for j, passage in enumerate(content["context"], 1):
                        st.markdown(f"> **Passage {j}:** {passage[:600]}{'…' if len(passage) > 600 else ''}")
                # Error dict
                elif "error" in content:
                    st.error(content["error"])
                # Weather / stock — clean key-value table
                else:
                    st.json(content, expanded=True)
            else:
                # Plain text results (web search, wikipedia)
                text = str(content)
                st.markdown(text[:1200] + ("…" if len(text) > 1200 else ""))

            if i < count - 1:
                st.divider()


# ---------------------------------------------------------------------------
# Main area — Chat + Architecture tabs
# ---------------------------------------------------------------------------
chat_tab, arch_tab = st.tabs(["💬 Chat", "🗺 Architecture"])

with chat_tab:
    st.title("🤖 Agentic RAG Chatbot")
    st.caption(
        "Azure OpenAI · LangGraph · SQLite · Web Search · Wikipedia · Weather · Stock Market · "
        "Built with LangGraph · Azure OpenAI · LangSmith · Streamlit · pypdf"
    )

    # Fixed-height scrollable container for all messages.
    # Keeps the chat input anchored below it instead of drifting to the middle.
    chat_area = st.container(height=560, border=False)

    with chat_area:
        for msg in st.session_state["message_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("Ask about your PDF, search the web, get weather, check stocks…")

    if user_input:
        st.session_state["message_history"].append({"role": "user", "content": user_input})

        if thread_key not in st.session_state["thread_titles"]:
            title = user_input.strip().replace("\n", " ")
            st.session_state["thread_titles"][thread_key] = (
                title[:45] + "…" if len(title) > 45 else title
            )

        run_config = {
            "configurable": {"thread_id": thread_key},
            "metadata": {"thread_id": thread_key},
            "run_name": "azure_rag_chat",
        }

        with chat_area:
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                _ctx: dict[str, Any] = {"status_box": None, "tool_results": []}

                # Generator that yields text tokens, shows live tool-call status,
                # and collects each tool result for the sources panel below
                def _stream_response():
                    for chunk, _ in chatbot.stream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=run_config,
                        stream_mode="messages",
                    ):
                        if isinstance(chunk, AIMessage) and chunk.tool_calls:
                            names = ", ".join(f"`{tc['name']}`" for tc in chunk.tool_calls)
                            if _ctx["status_box"] is None:
                                _ctx["status_box"] = st.status(f"🔧 Calling {names}…", expanded=True)
                            else:
                                _ctx["status_box"].update(label=f"🔧 Calling {names}…", state="running", expanded=True)
                        elif isinstance(chunk, ToolMessage):
                            _ctx["tool_results"].append({"tool": chunk.name, "content": chunk.content})
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

                # Sources panel — always visible below the answer when any tool was used
                if _ctx["tool_results"]:
                    _render_sources(_ctx["tool_results"])

            doc_meta = get_metadata(thread_key)
            if doc_meta:
                st.caption(
                    f"Document in context: **{doc_meta['filename']}** — "
                    f"{doc_meta['chunks']} chunks, {doc_meta['documents']} pages"
                )

        if ai_reply:
            st.session_state["message_history"].append({"role": "assistant", "content": ai_reply})

    if selected_thread:
        st.session_state["thread_id"] = selected_thread
        st.session_state["message_history"] = load_thread_conversation(selected_thread)
        st.session_state["ingested_docs"].setdefault(selected_thread, {})
        st.rerun()

with arch_tab:
    draw_architecture_tab(chatbot)
