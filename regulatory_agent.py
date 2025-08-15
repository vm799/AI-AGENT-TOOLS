# regulatory_agent.py
import os
import sys
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from langchain_openai import ChatOpenAI
#from langchain.tools.python.tool import PythonREPLTool

from tools import get_search_tool
from rag_tool import get_rag_tool


def main():
    # 1) Load environment variables (.env)
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to your .env file.")

    # 2) LLM (the model/brain)
    # Use a small, cheap, instruction-following chat model. You can swap models here.
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 3) Tools (capabilities the agent can call)
    #    a) Web search (fresh info)
    search = get_search_tool()

    #    b) Your Day-1 RAG (domain knowledge)
    rag_fn = get_rag_tool()

    #    c) Python REPL (math/data munging)
    py_repl = PythonREPLTool()

    tools = [
        Tool(
            name="WebSearch",
            func=search.run,
            description=(
                "Use for up-to-date info from the open web (news, websites, fresh facts). "
                "Great when the answer likely isn't in the local knowledge base."
            ),
        ),
        Tool(
            name="RegulatoryRAG",
            func=rag_fn,
            description=(
                "Use for questions about regulatory approvals and clinical trials contained "
                "in the local Chroma vector database (domain knowledge)."
            ),
        ),
        Tool(
            name="PythonREPL",
            func=py_repl.run,
            description=(
                "Use for calculations, quick data transforms, or validating numeric reasoning."
            ),
        ),
    ]

    # 4) Memory (so the agent remembers the conversation)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    # 5) Initialize the Agent (ReAct-style reasoning over tools)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,                 # show reasoning traces & tool calls
        handle_parsing_errors=True,   # be resilient to occasional model formatting hiccups
    )

    # 6) Run from CLI
    if len(sys.argv) < 2:
        print("Usage: python regulatory_agent.py 'Your question here'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = agent.run(query)
    print("\nFINAL ANSWER:\n", result)


if __name__ == "__main__":
    main()
