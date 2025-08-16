# langchain_template.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

# 1️⃣ Initialize chat model
chat_model = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# 2️⃣ Setup memory (optional, keeps conversation context)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 3️⃣ Define a prompt template
template = """
You are a helpful AI assistant.
Human: {user_input}
AI:
"""

prompt = PromptTemplate(input_variables=["user_input"], template=template)

# 4️⃣ Create LLM chain with memory
chain = LLMChain(llm=chat_model, prompt=prompt, memory=memory)

# 5️⃣ Run the chain
user_input = "Give me a creative idea for a productivity app."
response = chain.run(user_input)
print("AI:", response)

# 6️⃣ Add a follow-up to see memory in action
user_input2 = "Now give me a catchy name for it."
response2 = chain.run(user_input2)
print("AI:", response2)
