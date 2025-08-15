import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_community.tools import SerpAPIWrapper
    print("✅ SerpAPIWrapper import works")
except ImportError as e:
    print("❌ Import failed:", e)

