from typing import Literal
from agents import function_tool
from tavily import AsyncTavilyClient

from app.core.settings import settings


tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY) if settings.TAVILY_API_KEY else None


@function_tool
async def tavily_search(query: str, include_domains: list[str], max_results: int = 10, search_depth: Literal["basic", "advanced"] = "advanced") -> dict:
    """
    Search the web using Tavily API for real-time information.

    Use this tool when you need to find current information, news, facts, or
    research topics that require up-to-date web search results.

    Args:
        query (str): The search query string. Be specific for better results.
        max_results (int): Maximum number of search results to return (default: 5, max: 20).
        search_depth (str): Search depth level - "basic" for quick results or "advanced"
            for more comprehensive results (default: "basic").
        include_domains: (list[str]): Search web

    Returns:
        dict: A dictionary containing search results with the following keys:
            - query: The original search query
            - results: List of search results, each containing:
                - title: The title of the webpage
                - url: The URL of the webpage
                - content: A snippet/summary of the content
                - score: Relevance score
            - answer: An AI-generated answer based on search results (if available)


    Raises:
        Exception: If Tavily API key is not configured or API request fails.
    """
    if not tavily_client:
        raise ValueError("TAVILY_API_KEY is not configured in environment variables")

    response = await tavily_client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced",
        include_answer=True,
        include_domains=include_domains,
        include_raw_content="markdown"
    )
    return response


@function_tool
async def tavily_crawl(url: str, extract_depth: Literal["basic", "advanced"] = "basic") -> dict:
    """
    Crawl and extract content from a specific URL using Tavily API.

    Use this tool when you need to retrieve the full content from a specific
    webpage, documentation, article, or any URL.

    Args:
        url (str): The URL to crawl and extract content from.
        extract_depth (str): Extraction depth - "basic" for main content or "advanced"
            for more comprehensive extraction including nested content (default: "basic").

    Returns:
        dict: A dictionary containing crawled content with the following keys:
            - url: The crawled URL
            - raw_content: The extracted raw content from the webpage
            - images: List of image URLs found on the page (if any)
            - metadata: Additional metadata about the crawled page

    Raises:
        Exception: If Tavily API key is not configured, URL is invalid, or crawl fails.
    """
    if not tavily_client:
        raise ValueError("TAVILY_API_KEY is not configured in environment variables")

    response = await tavily_client.crawl(
        url=url,
        extract_depth=extract_depth,
    )
    return response


@function_tool
async def tavily_scrape(url: str) -> dict:
    """
    Scrape and extract structured content from a specific URL using Tavily API.

    Use this tool when you need to extract clean, structured content from a webpage.
    This is similar to crawl but optimized for extracting readable content like
    articles, blog posts, documentation, etc.

    Args:
        url (str): The URL to scrape and extract content from.

    Returns:
        dict: A dictionary containing scraped content with the following keys:
            - url: The scraped URL
            - content: The clean, extracted content from the webpage
            - title: The title of the webpage
            - metadata: Additional metadata including author, publish date, etc.

    Raises:
        Exception: If Tavily API key is not configured, URL is invalid, or scrape fails.
    """
    if not tavily_client:
        raise ValueError("TAVILY_API_KEY is not configured in environment variables")

    response = await tavily_client.extract(
        urls=[url],
    )
    return response
