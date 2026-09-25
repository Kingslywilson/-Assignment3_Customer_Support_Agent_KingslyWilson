# Autonomous Customer Support Agent - Strategy

## 1. Overview

This project implements an autonomous customer support agent built with **Python 3.11+**, **LangChain**, and **ChatGroq**.

The agent handles:
- Order status queries and delivery tracking
- Product searches with combined keyword matching and price/attribute filtering
- Frequently asked questions (FAQ) search
- Return and refund policy queries
- Multi-turn conversations with isolated memory
- Multi-tool execution for compound requests
- Graceful handling of unknown or missing information
- Tool errors with an explicit 2-retry mechanism and graceful fallback
- Progressive streaming and observable full-lifecycle callbacks
- Production tracing via LangSmith

---

## 2. Agent Architecture

The main project components are:
- `app.py` - CLI interaction entrypoint implementing progressive response streaming (`agent_executor.stream`).
- `agent.py` - LangChain agent initialization (`ChatGroq`, `ChatPromptTemplate`, `create_tool_calling_agent`, `AgentExecutor`).
- `memory.py` - Session message history container managing `HumanMessage` and `AIMessage` objects.
- `session_manager.py` - Session manager enforcing memory isolation across unique session IDs.
- `callbacks.py` - `SupportAgentCallback` handling the full lifecycle (Agent Start, LLM Start, Tool Start, Tool End, Tool Error, LLM End, Agent End) without exposing prompt secrets or internal reasoning.
- `tools/retry_handler.py` - `@with_tool_retry(max_retries=2)` decorator executing tool retries and graceful fallback.
- `tools/` - Custom support tools (`order_status.py`, `product_search.py`, `faq_search.py`, `return_policy.py`).
- `data/` - Mock JSON data stores (`orders.json`, `products.json`, `faq.json`, `return_policy.json`).
- `prompts/agent_prompt.txt` - System instructions for customer support behavior and safety constraints.

---

## 3. Custom Support Tools

### Order Status Tool (`tools/order_status.py`)
- Purpose: Retrieve status, expected delivery date, and carrier for order IDs starting with `ORD`.
- Protection: Validates order ID formatting and returns error messages for invalid formats or unknown orders without hallucinating data. Includes simulated retry test paths.

### Product Search Tool (`tools/product_search.py`)
- Purpose: Search product catalog based on product name, category, description, features, color, availability, or price limits.
- Price & Attribute Filter Fix: Employs strict combined **AND logic** (matching both keywords and numeric price constraints like `"wireless headphones under ₹5,000"`).

### FAQ Search Tool (`tools/faq_search.py`)
- Purpose: Search predefined support FAQ items covering shipping, payment, order modifications, cancellation, warranty, account management, and support channels.

### Return Policy Tool (`tools/return_policy.py`)
- Purpose: Provide exact return policy details (standard return period, refund timelines, opened electronics rules, unused conditions, return fees, damaged products, exceptions).

---

## 4. Tool Retry & Failure Handling (`tools/retry_handler.py`)

- **Maximum Retries**: Exactly 2 retries (total 3 attempts).
- **Temporary Failure Recovery**: When a tool encounters a temporary network, database, or runtime exception, the wrapper logs a retry warning, waits briefly, and retries execution.
- **Graceful Fallback**: If a tool fails on all 3 attempts (initial attempt + 2 retries), the retry handler catches the exception and returns a user-friendly fallback message:
  > *"We are currently experiencing temporary technical issues with this service. Please try again later."*

---

## 5. Progressive Streaming (`app.py`)

- Uses `agent_executor.stream(...)` to stream response chunks progressively to the user console.
- Output tokens and execution steps appear live without blocking the terminal interface until completion.

---

## 6. Lifecycle Callbacks (`callbacks.py`)

The custom `SupportAgentCallback` handler hooks into the full execution lifecycle:
1. `on_chain_start` -> `[AGENT START]`
2. `on_llm_start` -> `[LLM START]` (Logs model invocation without exposing internal system prompts)
3. `on_tool_start` -> `[TOOL START]` & `[TOOL INPUT]`
4. `on_tool_end` -> `[TOOL END]` & `[TOOL RESULT]`
5. `on_tool_error` -> `[TOOL ERROR]`
6. `on_llm_end` -> `[LLM END]`
7. `on_agent_finish` -> `[AGENT END]`

Confidentiality & Safety: Internal chain-of-thought reasoning, API keys, and prompt instructions are kept private and omitted from output logs.

---

## 7. Conversation Memory & Session Isolation

- **Memory**: `ConversationMemory` stores structured `HumanMessage` and `AIMessage` objects.
- **Prompt Integration**: `agent.py` injects previous message history into `ChatPromptTemplate` using `MessagesPlaceholder(variable_name="chat_history")`.
- **Session Isolation**: `SessionManager` maintains a dictionary mapping `session_id` to separate `ConversationMemory` instances, preventing cross-session memory leakage.

---

## 8. LangSmith Observability

LangSmith tracing is configured using current environment variable standards:
- `LANGSMITH_TRACING=true`
- `LANGSMITH_API_KEY=your_langsmith_api_key_here`
- `LANGSMITH_PROJECT=Assignment3-Customer-Support-Agent`

Legacy aliases (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`) are maintained for backward compatibility.

---

## 9. Security & Safety

- Uses mock customer support data only.
- Strict instructions prohibit requesting or revealing sensitive user data (passwords, OTPs, CVV, PINs, card numbers, API keys).
- API credentials stored exclusively in `.env` (git-ignored via `.gitignore`).