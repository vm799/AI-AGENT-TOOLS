# rag_tool.py
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import OpenAI
import os

def get_rag_tool():
    """Loads the RAG pipeline as a LangChain Tool."""
    
    # Load the vector database from Day 1
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory="vector_db", embedding_function=embeddings)
    
    # Create RetrievalQA chain
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        chain_type="stuff"
    )
    
    # Return the chain as a callable function
    def rag_search(query: str) -> str:
        return qa_chain.run(query)
    
    return rag_search
