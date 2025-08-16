# test_tools.py
from dotenv import load_dotenv
load_dotenv()  # load .env keys

from tools import get_search_tool, get_python_tool

search = get_search_tool()
python_tool = get_python_tool()

print("✅ All tools imported successfully")
print("Testing SerpAPI query...")
print(search.run("Capital of France?"))
