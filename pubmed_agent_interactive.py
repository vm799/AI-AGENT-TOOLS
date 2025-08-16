# pubmed_agent_interactive.py
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Step 1: Query PubMed ---
def search_pubmed(query, max_results=3):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "xml", "retmax": max_results}
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    ids = [id_tag.text for id_tag in soup.find_all("id")]
    return ids

# --- Step 2: Fetch abstracts ---
def fetch_abstracts(pubmed_ids):
    abstracts = []
    for pmid in pubmed_ids:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pubmed", "id": pmid, "retmode": "xml"}
        r = requests.get(url, params=params)
        soup = BeautifulSoup(r.text, "lxml")
        abstract_tag = soup.find("abstract")
        title_tag = soup.find("article-title")
        if abstract_tag:
            abstracts.append({
                "pmid": pmid,
                "title": title_tag.text if title_tag else "No title",
                "abstract": abstract_tag.text
            })
    return abstracts

# --- Step 3: Summarize with OpenAI ---
def summarize_abstracts(abstracts):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    template = PromptTemplate(
        input_variables=["title", "abstract"],
        template="Summarize the following medical abstract in 2 sentences:\n\nTitle: {title}\nAbstract: {abstract}\nSummary:"
    )
    chain = LLMChain(llm=llm, prompt=template)
    
    summaries = []
    for item in abstracts:
        summary = chain.run(title=item["title"], abstract=item["abstract"])
        summaries.append({"pmid": item["pmid"], "summary": summary})
    return summaries

# --- Step 4: Interactive CLI ---
def run_agent():
    print("=== PubMed Summarizer Agent ===")
    while True:
        query = input("\nEnter drug or medical term (or 'exit' to quit): ")
        if query.lower() in ["exit", "quit"]:
            print("Exiting agent. Goodbye!")
            break
        
        print(f"\nSearching PubMed for: {query} ...")
        ids = search_pubmed(query)
        if not ids:
            print("No results found.")
            continue
        
        abstracts = fetch_abstracts(ids)
        summaries = summarize_abstracts(abstracts)
        
        print("\n--- Summaries ---")
        for s in summaries:
            print(f"PMID: {s['pmid']}\nSummary: {s['summary']}\n{'-'*40}")

if __name__ == "__main__":
    run_agent()
