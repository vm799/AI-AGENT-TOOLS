# tools.py
import os
from langchain.tools.python.tool import PythonREPLTool  # Correct for langchain 0.3.27
from langchain.tools.serpapi import SerpAPIWrapper  # Correct for langchain-community 0.3.27

def get_search_tool():
    """Returns a SerpAPI search tool."""
    serp_api_key = os.getenv("SERPAPI_API_KEY")
    if not serp_api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment variables.")
    
    return SerpAPIWrapper(serpapi_api_key=serp_api_key)


def get_python_tool():
    """Returns a Python REPL tool for code execution."""
    return PythonREPLTool()
