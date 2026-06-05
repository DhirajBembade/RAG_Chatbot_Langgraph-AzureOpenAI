# tools.py
# Defines all five tools that the LangGraph agent can call:
#   - duckduckgo_search  : live web search via DuckDuckGo (no API key needed)
#   - wikipedia_search   : encyclopedic lookups via Wikipedia API
#   - get_weather        : current weather for any city using wttr.in (free)
#   - get_stock_price    : live stock quotes via Alpha Vantage (free API key required)
#   - rag_search         : similarity search over the user's uploaded PDF (FAISS)
#
# TOOLS list and llm_with_tools are imported by graph.py to build the LangGraph agent.

from __future__ import annotations

import os
from typing import Annotated

import requests
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, tool

from config import llm
from rag import get_metadata, get_retriever

duckduckgo_search = DuckDuckGoSearchRun(region="us-en", name="duckduckgo_search")

_wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=2000),
)


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for encyclopedic facts and background knowledge.

    Args:
        query: The topic or question to look up on Wikipedia
    """
    try:
        return _wikipedia.run(query)
    except Exception as e:
        return f"Wikipedia search failed ({type(e).__name__}: {e}). Try duckduckgo_search instead."


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city. Returns temperature, humidity, wind speed, and conditions.

    Args:
        city: City name (e.g. 'Mumbai', 'London', 'New York')
    """
    try:
        r = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()
        data = r.json()
        current = data["current_condition"][0]
        area = data.get("nearest_area", [{}])[0]
        return {
            "city": (
                f"{area.get('areaName', [{}])[0].get('value', city)}, "
                f"{area.get('country', [{}])[0].get('value', '')}"
            ),
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
    """Fetch the latest share/stock price and quote data for a ticker symbol.

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
    try:
        r = requests.get(
            "https://www.alphavantage.co/query",
            params={"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key},
            timeout=10,
        )
        r.raise_for_status()
        quote = r.json().get("Global Quote", {})
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
    retriever = get_retriever(thread_id)
    if retriever is None:
        return {
            "error": "No document indexed for this session. Please upload a PDF first.",
            "query": query,
        }
    docs = retriever.invoke(query)
    return {
        "query": query,
        "source_file": get_metadata(thread_id).get("filename"),
        "context": [doc.page_content for doc in docs],
        "metadata": [doc.metadata for doc in docs],
    }


# Bind all tools to the LLM so the model can emit tool_calls in its responses
TOOLS = [duckduckgo_search, wikipedia_search, get_weather, get_stock_price, rag_search]
llm_with_tools = llm.bind_tools(TOOLS)
