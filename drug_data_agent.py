# drug_data_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pandas as pd

# 1️⃣ Example tool: Query drug trial CSV
def query_drug_trials(drug_name: str) -> str:
    """
    Reads a CSV of clinical trials and returns relevant info for the drug.
    """
    try:
        df = pd.read_csv("drug_trials.csv")  # Your clinical trials dataset
        result = df[df['drug'].str.contains(drug_name, case=False)]
        if result.empty:
            return f"No trials found for {drug_name}."
        return result.to_string(index=False)
    except Exception as e:
        return f"Error accessing drug trials data: {e}"

# 2️⃣ Wrap it as a LangChain Tool
drug_trials_tool = Tool(
    name="DrugTrialsQuery",
    func=query_drug_trials,
    description="Use this tool to get clinical trial info for a specific drug."
)

# 3️⃣ Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 4️⃣ Optional prompt template
prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a drug trial assistant. Answer the following query accurately:\n{query}"
)

# 5️⃣ Optional LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# 6️⃣ Initialize the agent with tools
agent = initialize_agent(
    tools=[drug_trials_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# 7️⃣ Example query
query = "Tell me about clinical trials for Ibuprofen"
response = agent.run(query)
print(response)

