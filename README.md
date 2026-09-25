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

Install the required dependencies:

pip install -r requirements.txt

Create a .env file using .env.example as a reference.

Add your API keys:

GROQ_API_KEY=your_groq_api_key

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=Assignment3-Customer-Support-Agent

Do not share or commit the .env file.

Run

Start the application:

python app.py

Enter a session ID when prompted.

Example:

Session ID: customer1

Then ask questions such as:

What is the status of order ORD1005?

or:

How long does standard delivery take?

Type exit to close the application.

Supported Operations
Order Status

The agent can check:

Order status
Expected delivery
Carrier information
Product Search

The agent can search products by:

Product name
Category
Features
Price
Availability
FAQ

The agent can answer configured questions about:

Shipping
Payment
Order modification
Cancellation
Warranty
Account information
Customer support
Return Policy

The agent can provide configured information about:

Return period
Refund timeline
Return eligibility
Opened electronics
Damaged products
Return charges
Exceptions
Testing

The project was tested for:

Order status
Product search
FAQ search
Return policy
Multi-tool requests
Multi-turn conversations
Session isolation
Unknown orders
Unknown products
Missing information
Invalid order IDs
Tool failures
Controlled retry
Execution limits
Streaming
Callbacks
LangSmith tracing
Security handling

Detailed test results are available in test_log.md.

Security

This project uses mock customer support data only.

The agent must not request or expose:

Passwords
OTPs
CVV
PINs
Full card numbers
Authentication tokens
API keys

API keys are stored in .env and are excluded from version control using .gitignore.

Technology
Python 3.11
LangChain
LangChain Groq
Groq
Pydantic
LangSmith
python-dotenv