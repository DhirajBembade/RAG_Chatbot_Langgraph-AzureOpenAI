# diagrams.py
# Renders the Architecture tab in the Streamlit app.
# Left panel: LangGraph native Mermaid state-machine diagram.
# Right panel: Matplotlib full system flow diagram.

from __future__ import annotations

import streamlit as st


def draw_architecture_tab(chatbot) -> None:
    st.markdown("### How It Works")

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("#### LangGraph State Machine")
        try:
            img_bytes = chatbot.get_graph().draw_mermaid_png()
            st.image(img_bytes, use_container_width=True)
        except Exception:
            st.code(chatbot.get_graph().draw_mermaid())
            st.caption("Paste into [mermaid.live](https://mermaid.live) to render")

    with col_r:
        st.markdown("#### Full System Flow")
        import matplotlib.pyplot as plt
        fig = _build_fig()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.divider()
    _draw_flow_explanation()


def _build_fig():
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

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
    ax.text(0.5, 2.5, "📄 PDF Upload\n→ pypdf\n→ FAISS chunks",
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


def _draw_flow_explanation() -> None:
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
