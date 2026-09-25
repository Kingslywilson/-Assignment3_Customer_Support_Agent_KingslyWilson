import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.order_status import order_status_tool
from tools.product_search import product_search_tool
from tools.faq_search import faq_search_tool
from tools.return_policy import return_policy_tool
from session_manager import SessionManager


load_dotenv()

tools = [
    order_status_tool,
    product_search_tool,
    faq_search_tool,
    return_policy_tool,
]

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

with open("prompts/agent_prompt.txt", "r", encoding="utf-8") as file:
    agent_instructions = file.read()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", agent_instructions),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    max_execution_time=30,
    handle_parsing_errors=True,
)

session_manager = SessionManager()