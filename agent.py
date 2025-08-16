# agent.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Tools
from tools import get_search_tool, get_python_tool

class AIWorkspace:
    """Optimized AI Agent Skeleton."""

    def __init__(self):
        self.tools = {}
        self._load_tools()

    def _load_tools(self):
        """Initialize all tools and validate environment keys."""
        # Initialize SerpAPI search tool
        try:
            self.tools["search"] = get_search_tool()
        except Exception as e:
            raise RuntimeError(f"Error initializing search tool: {e}")

        # Initialize Python REPL tool
        try:
            self.tools["python"] = get_python_tool()
        except Exception as e:
            raise RuntimeError(f"Error initializing Python tool: {e}")

        print("✅ All tools loaded successfully!")

    def run_search(self, query: str):
        """Run a search query using SerpAPI."""
        if "search" not in self.tools:
            raise RuntimeError("Search tool not available.")
        return self.tools["search"].run(query)

    def run_python(self, code: str):
        """Run Python code dynamically."""
        if "python" not in self.tools:
            raise RuntimeError("Python tool not available.")
        return self.tools["python"].run(code)

def main():
    # Initialize workspace
    try:
        workspace = AIWorkspace()
    except RuntimeError as e:
        print(f"❌ Workspace initialization failed: {e}")
        return

    # Example search
    try:
        query = "Latest AI agent news"
        results = workspace.run_search(query)
        print("🔎 Search Results:", results)
    except Exception as e:
        print(f"❌ Search failed: {e}")

    # Example Python execution
    try:
        code = "sum(range(1, 6))"  # Example: 1+2+3+4+5
        result = workspace.run_python(code)
        print("🧮 Python Execution Result:", result)
    except Exception as e:
        print(f"❌ Python execution failed: {e}")

if __name__ == "__main__":
    main()
