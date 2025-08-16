# fetch_trials.py
import os

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# -----------------------------
# CONFIG
# -----------------------------
# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"


# -----------------------------
# FUNCTIONS
# -----------------------------

def fetch_pubmed_articles(query: str, max_results: int = 10):
    """
    Fetch articles from PubMed based on a search query.
    """
    results = pubmed.query(query, max_results=max_results)
    articles = []

    for article in results:
        abstract = article.abstract or ""
        title = article.title or ""
        authors = ", ".join([str(a) for a in article.authors]) if article.authors else ""
        journal = article.journal or ""
        year = article.year or ""

        content = f"Title: {title}\nAuthors: {authors}\nJournal: {journal}\nYear: {year}\nAbstract: {abstract}"
        articles.append(Document(page_content=content))

    return articles


def create_embeddings_and_store(documents):
    """
    Split long texts, generate embeddings, and store in Chroma vector DB.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embeddings, collection_name="medical_trials")
    return vectordb


def query_medical_data(vectordb, query: str):
    """
    Query stored medical articles using OpenAI Chat model.
    """
    chat = ChatOpenAI(model_name="gpt-4", temperature=0)
    docs = vectordb.similarity_search(query, k=3)

    answers = []
    for doc in docs:
        response = chat.predict(f"Summarize the key points from this document:\n{doc.page_content}")
        answers.append(response)

    return answers


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    search_term = "COVID-19 vaccine clinical trials"
    print(f"Fetching articles for: {search_term}")
    articles = fetch_pubmed_articles(search_term, max_results=5)
    print(f"Fetched {len(articles)} articles ✅")

    print("Creating embeddings and vector store...")
    vectordb = create_embeddings_and_store(articles)
    print("Vector store ready ✅")

    query = "Summarize safety and efficacy findings"
    print(f"Querying vector store: {query}")
    results = query_medical_data(vectordb, query)

    for i, res in enumerate(results, 1):
        print(f"\nResult {i}:\n{res}\n{'-'*50}")
# This script fetches clinical trial articles from PubMed, processes them, and allows querying using a vector database.