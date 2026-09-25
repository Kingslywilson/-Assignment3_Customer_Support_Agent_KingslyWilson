# Autonomous Customer Support Agent

An autonomous customer support agent built using Python, LangChain, and Groq.

## Features

- Order status lookup
- Product search
- FAQ search
- Return and refund policy
- Multi-turn conversations
- Multi-tool execution
- Session isolation
- Error handling
- Controlled retry
- Execution limits
- Streaming
- Custom callbacks
- LangSmith tracing
- Input validation
- Security handling

## Project Structure

```text
Assignment3_Customer_Support_Agent_KingslyWilson/
│
├── app.py
├── agent.py
├── memory.py
├── session_manager.py
├── callbacks.py
│
├── tools/
│   ├── __init__.py
│   ├── order_status.py
│   ├── product_search.py
│   ├── faq_search.py
│   └── return_policy.py
│
├── prompts/
│   └── agent_prompt.txt
│
├── data/
│   ├── orders.json
│   ├── products.json
│   ├── faq.json
│   └── return_policy.json
│
├── agent_strategy.md
├── test_log.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore

Setup

Create and activate a Python virtual environment.

Install dependencies:

pip install -r requirements.txt

Create a .env file from .env.example.

Add:

GROQ_API_KEY=your_groq_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=Assignment3-Customer-Support-Agent
Run

Start the application with:

python app.py
Testing

The project includes tests for:

Order status
Product search
FAQ
Return policy
Multi-tool requests
Multi-turn conversations
Session isolation
Unknown information
Tool retry
Streaming
Callbacks
LangSmith tracing
Security
Security

This project uses mock customer support data.

Do not store real passwords, OTPs, CVV, PINs, card numbers, API keys, or authentication tokens in the project.

The .env file is excluded from version control.

Technology
Python
LangChain
LangChain Groq
Groq
Pydantic
LangSmith
python-dotenv

---

# 5. `.env.example`

Use:

```text
GROQ_API_KEY=your_groq_api_key_here

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=Assignment3-Customer-Support-Agent

Do not put your real API keys in .env.example.