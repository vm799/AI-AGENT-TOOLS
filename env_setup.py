# env_setup.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Optional: quick check
required_vars = ["SERPAPI_API_KEY"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} not found in environment variables")
