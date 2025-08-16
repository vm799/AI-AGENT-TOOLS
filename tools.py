# tools.py
import os
from langchain.utilities import SerpAPIWrapper
from langchain.tools import PythonREPLTool

def get_search_tool():
    """Returns a SerpAPI search tool."""
    serp_api_key = os.getenv("SERPAPI_API_KEY")
    if not serp_api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment variables.")
    
    return SerpAPIWrapper(serpapi_api_key=serp_api_key)

def get_python_tool():
    """Returns a Python REPL tool."""
    return PythonREPLTool()
