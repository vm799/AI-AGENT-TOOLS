# tools.py
# Old (broken)
# from langchain_community.tools import SerpAPIWrapper

# New (works)
from langchain_community.tools.serpapi import SerpAPIWrapper


def get_search_tool():
    """Returns a SerpAPI search tool."""
    serp_api_key = os.getenv("SERPAPI_API_KEY")
    if not serp_api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment variables.")
    
    search = SerpAPIWrapper(serpapi_api_key=serp_api_key)
    return search
