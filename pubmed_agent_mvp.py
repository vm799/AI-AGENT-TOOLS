# pubmed_agent_mvp.py

# 1️⃣ Load environment variables
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # reads your .env file

# 2️⃣ Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Optional: debug to check key is loaded
print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))

# 3️⃣ Rest of your imports
import requests

# 4️⃣ Your functions
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize this: {text}"}]
    )
    return response.choices[0].message.content

# 5️⃣ Your main code
if __name__ == "__main__":
    abstract = "Some sample PubMed abstract text here..."
    summary = summarize_text(abstract)
    print(summary)
exit
