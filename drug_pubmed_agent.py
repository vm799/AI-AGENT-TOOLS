# drug_pubmed_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup

# 1️⃣ Tool: Query PubMed abstracts
def query_pubmed(drug_name: str, max_results=3) -> str:
    """
    Searches PubMed for the drug and returns abstracts.
    """
    try:
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={drug_name}&format=abstract"
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error fetching PubMed data: {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='docsum-content')[:max_results]
        if not articles:
            return f"No articles found for {drug_name}."
        
        results = []
        for art in articles:
            title = art.find('a', class_='docsum-title').get_text(strip=True)
            snippet = art.find('div', class_='full-view-snippet').get_text(strip=True)
            results.append(f"{title}: {snippet}")
        
        return "\n\n".join(results)
    except Exception as e:
        return f"Error: {e}"

# 2️⃣ Wrap it as a LangChain Tool
pubmed_tool = Tool(
    name="PubMedQuery",
    func=query_pubmed,
    description="Fetches PubMed abstracts for a given drug."
)

# 3️⃣ Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 4️⃣ Optional prompt template
prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a drug information assistant. Answer accurately:\n{query}"
)

# 5️⃣ Optional LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# 6️⃣ Initialize the agent
agent = initialize_agent(
    tools=[pubmed_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# 7️⃣ Example query
query = "Find clinical trial info for Ibuprofen"
response = agent.run(query)
print(response)
