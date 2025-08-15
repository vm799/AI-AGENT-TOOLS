# main_build.py
import os
from tools import get_search_tool, get_python_tool

# Load environment variables (if using a .env file)
from dotenv import load_dotenv
load_dotenv()

def main():
    # Initialize tools
    try:
        search_tool = get_search_tool()
        python_tool = get_python_tool()
        print("✅ Tools loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading tools: {e}")
        return

    # Example usage of SerpAPIWrapper
    try:
        query = "Latest news on AI agents"
        print(f"Searching for: {query}")
        search_results = search_tool.run(query)
        print("Search results:", search_results)
    except Exception as e:
        print(f"❌ Search tool error: {e}")

    # Example usage of PythonREPLTool
    try:
        code = "2 + 2"
        print(f"Running code: {code}")
        python_result = python_tool.run(code)
        print("Python tool result:", python_result)
    except Exception as e:
        print(f"❌ Python tool error: {e}")

if __name__ == "__main__":
    main()
