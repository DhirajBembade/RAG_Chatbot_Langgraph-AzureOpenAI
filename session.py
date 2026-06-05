# session.py
# Thread/conversation helpers that sit on top of the LangGraph checkpointer.
#
# retrieve_all_threads()       — lists every thread_id stored in SQLite (for the sidebar)
# load_thread_conversation()   — replays a thread's message history as plain dicts
# get_thread_title()           — derives a human-readable title from the first user message

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage

from graph import chatbot, checkpointer


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


def get_thread_title(thread_id: str) -> str:
    for msg in load_thread_conversation(thread_id):
        if msg["role"] == "user" and msg["content"].strip():
            title = msg["content"].strip().replace("\n", " ")
            return title[:45] + "…" if len(title) > 45 else title
    return f"New chat {thread_id[:6]}…"
