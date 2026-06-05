# graph.py
# Builds and compiles the LangGraph state machine that powers the chatbot.
#
# Graph topology (compiled as `chatbot`):
#   __start__ → chat_node → tools_condition ─┬─ (tool_calls) → ToolNode → chat_node (loop)
#                                             └─ (no tools)   → __end__
#
# Key components:
#   - ChatState       : TypedDict holding the running list of messages
#   - SYSTEM_PROMPT   : injected at the start of every LLM call
#   - chat_node       : calls Azure OpenAI with the current message history
#   - tool_node       : executes whichever tools the LLM requested
#   - checkpointer    : SQLite-backed persistence so chats survive restarts
#   - chatbot         : the compiled, runnable LangGraph graph

from __future__ import annotations

import sqlite3
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools import TOOLS, llm_with_tools


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
    # Azure OpenAI returns HTTP 400 if an AIMessage with tool_calls lacks
    # the corresponding ToolMessages. This strips any such incomplete pairs
    # before re-sending the history to the LLM.
    result: list[BaseMessage] = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        if isinstance(msg, AIMessage) and msg.tool_calls:
            expected = {tc["id"] for tc in msg.tool_calls}
            j = i + 1
            found: dict[str, ToolMessage] = {}
            while j < len(messages) and isinstance(messages[j], ToolMessage):
                found[messages[j].tool_call_id] = messages[j]
                j += 1
            if expected <= found.keys():
                result.append(msg)
                result.extend(found[tid] for tid in expected)
            i = j
        elif isinstance(msg, ToolMessage):
            i += 1
        else:
            result.append(msg)
            i += 1
    return result


def chat_node(state: ChatState, config=None):
    clean = _sanitize_messages(list(state["messages"]))
    return {"messages": [llm_with_tools.invoke([SYSTEM_PROMPT, *clean], config=config)]}


tool_node = ToolNode(
    TOOLS,
    handle_tool_errors=lambda e: f"Tool error ({type(e).__name__}): {e}",
)

# Persistent SQLite checkpointer — stores every state snapshot so conversations
# can be resumed after a Streamlit restart
_db_conn = sqlite3.connect(database="azure_chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=_db_conn)

# Wire up the graph: START → chat_node ↔ ToolNode (loop), or → __end__
_builder = StateGraph(ChatState)
_builder.add_node("chat_node", chat_node)
_builder.add_node("tools", tool_node)
_builder.add_edge(START, "chat_node")
_builder.add_conditional_edges("chat_node", tools_condition)
_builder.add_edge("tools", "chat_node")

chatbot = _builder.compile(checkpointer=checkpointer)
