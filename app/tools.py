
import os
from tavily import TavilyClient


def search_web(query: str) -> list:
    """Search the web using Tavily and return relevant results."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing")

    client = TavilyClient(api_key=api_key)

    max_results = int(os.getenv("TAVILY_MAX_RESULTS", "5"))

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0)
        })

    return results
