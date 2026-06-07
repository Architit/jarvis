# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from langchain.tools import tool
from duckduckgo_search import DDGS

@tool("duckduckgo_search", return_direct=True)
def duckduckgo_search_tool(query: str) -> str:
    """
    Perform a web search using DuckDuckGo and return the top result.
    Use this tool when the user asks a question that requires up-to-date information from the internet.
    
    Examples of queries:
    - "Please look up what's the weather like in Paris today?"
    - "Look up the latest tech news"
    - "yes, please search for current AI news"

    Input:
    - A natural language query string.
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=1)
        results_list = list(results)

    if not results_list:
        return f"Apologies, I couldn't find any results for: \"{query}\"."

    top = results_list[0]
    return (
        f"Certainly sir, here's the top result for: \"{query}\"\n\n"
        f"🔹 Title: {top['title']}\n"
        f"🔗 URL: {top['href']}\n"
    )
