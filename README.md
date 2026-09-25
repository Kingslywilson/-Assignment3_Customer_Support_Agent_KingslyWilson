# Autonomous Customer Support Agent

An autonomous customer support agent built using **Python 3.11+**, **LangChain**, and **ChatGroq**.

## Overview & Architecture

The system uses `create_tool_calling_agent` paired with `AgentExecutor` to handle customer inquiries dynamically.

### Key Capabilities

* **Order Status Lookup**: Track order status, expected delivery, and carrier details.

* **Product Search**: Perform combined keyword and price filter searches (e.g. *"wireless headphones under ₹5,000"*), with support for category, feature, color, and availability filtering.

* **FAQ Search**: Search the knowledge base for policies regarding shipping, payment, warranty, and account management.

* **Return Policy**: Retrieve standard return windows, refund timelines, opened electronics policies, damaged item handling, and fees.

* **Multi-Turn Memory**: Retain context across turns using `HumanMessage` and `AIMessage` history in `MessagesPlaceholder(variable_name="chat_history")`.

* **Session Isolation**: Maintain independent conversation sessions via `SessionManager`.

* **Real Tool Retries**: Tool failure wrapper retry mechanism with **Maximum Retries = 2** (3 total attempts). Falls back gracefully after 2 retries with:

  > "We are currently experiencing temporary technical issues with this service. Please try again later."

* **Real Streaming**: Progressive execution and response-chunk streaming using `agent_executor.stream(...)`.

* **Full-Lifecycle Callbacks**: Custom `SupportAgentCallback` covering Agent Start, LLM Start, Tool Start, Tool End, Tool Error, LLM End, and Agent End without exposing prompt secrets or chain-of-thought reasoning.

* **LangSmith Tracing**: LangSmith tracing using `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, and `LANGSMITH_PROJECT`.

---

## Technical Stack & Version Requirements

* **Python**: `3.11+`

* **LangChain**: `langchain >= 0.3.0`, `langchain-core >= 0.3.0`, `langchain-groq >= 0.2.0`

* **LLM Provider**: ChatGroq (`openai/gpt-oss-20b` or `llama-3.3-70b-versatile`)

* **Environment Management**: `python-dotenv`

* **Data Validation**: `pydantic >= 2.0`

---

## Project Structure

```text
Assignment3_Customer_Support_Agent_KingslyWilson/

│
├── app.py                  # CLI application with real response streaming
├── agent.py                # Agent & AgentExecutor setup with LangSmith config
├── memory.py               # ConversationMemory using HumanMessage/AIMessage
├── session_manager.py      # Multi-session memory management
├── callbacks.py             # SupportAgentCallback full lifecycle handler
├── agent_strategy.md       # Comprehensive architectural strategy document
├── test_log.md              # Empirical test execution logs
├── README.md                # Project documentation
├── requirements.txt         # Python package dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Ignored files (.env, venv, pycache)
│
├── tools/                    # Custom tools with @with_tool_retry(max_retries=2)
│   ├── __init__.py
│   ├── retry_handler.py      # Retry decorator & graceful fallback handler
│   ├── order_status.py       # Order status lookup tool
│   ├── product_search.py     # Product search with combined price+keyword filtering
│   ├── faq_search.py         # FAQ search tool
│   └── return_policy.py      # Return policy lookup tool
│
├── prompts/
│   └── agent_prompt.txt      # System prompt
│
└── data/                     # Mock JSON data stores
    ├── orders.json
    ├── products.json
    ├── faq.json
    └── return_policy.json
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kingslywilson/-Assignment3_Customer_Support_Agent_KingslyWilson.git
cd Assignment3_Customer_Support_Agent_KingslyWilson
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```ini
GROQ_API_KEY=your_groq_api_key_here

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=Assignment3-Customer-Support-Agent
```

---

## How to Run

### Interactive Application

Run the interactive CLI with streaming:

```bash
python app.py
```

Enter a session ID (for example, `customer1`), then type questions such as:

* *"Can you find wireless headphones under ₹5,000?"*
* *"What is the status of order ORD1005?"*
* *"How many days do I have to return a product?"*

---

## Security

* This project uses mock data only.
* Strict prompt rules prevent requesting or outputting passwords, OTPs, CVV, PINs, card numbers, tokens, or API keys.
* Secrets are stored strictly in `.env` and excluded from Git via `.gitignore`.
