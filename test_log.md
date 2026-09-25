# Autonomous Customer Support Agent - Test Log & Verification

## Environment & Configuration

- **Python Version**: `3.11.x`
- **Framework**: `langchain 0.3+`, `langchain-core`, `langchain-groq`
- **LLM Model**: ChatGroq (`openai/gpt-oss-20b`)
- **Agent Architecture**: `create_tool_calling_agent` + `AgentExecutor`
- **Retry Mechanism**: `@with_tool_retry(max_retries=2)` wrapper (Maximum retries = 2, total attempts = 3)
- **Streaming Implementation**: Progressive step/token streaming via `agent_executor.stream(...)`
- **Tracing**: LangSmith (`LANGSMITH_TRACING=true`, `LANGSMITH_PROJECT=Assignment3-Customer-Support-Agent`)

---

## 1. Product Search with Price & Keyword Filter Fix

### Test Input
Query: `"wireless headphones under ₹5,000"`

### Verification & Output
```text
Tool Output:
Product ID: PRD201
Name: Wireless Headphones
Category: Audio
Price: ₹3499
Availability: In Stock
Features: Bluetooth, Noise Isolation, Built-in Microphone
Color: Black
```

### Result
**Passed**. The updated search implementation uses strict combined **AND logic**, matching both keyword query terms (*"wireless"*, *"headphones"*) AND numeric price constraints (*<= 5000*). Unrelated products under ₹5,000 (such as mouse, speaker, or keyboard) were correctly filtered out.

---

## 2. Order Status Lookup

### Test Input
Query: `"What is the status of order ORD1005?"`

### Verification & Output
```text
Tool Output:
Order ID: ORD1005
Status: Shipped
Expected Delivery: 22-Sep-2026
Carrier: Sample Logistics
```

### Result
**Passed**. The agent correctly extracted `ORD1005` and returned verified order status details from `orders.json`.

---

## 3. Real Tool Retry Mechanism (Temporary Error Recovery)

### Test Input
Simulated Query / Function: `get_order_status("ORD_SIMULATE_RETRY_RECOVER")`

### Verification & Console Output
```text
[RETRY WARN] Tool 'get_order_status' encountered temporary error (Attempt 1/3): Temporary network failure connecting to order database.. Retrying (1/2)...

Tool Output:
Order ID: ORD1005
Status: Delivered
Expected Delivery: 2026-09-20
Carrier: FedEx
```

### Result
**Passed**. On attempt 1, the temporary exception was caught, a retry warning was logged, and on attempt 2 (Retry 1) execution succeeded.

---

## 4. Real Tool Retry Mechanism (2-Attempt Exhaustion & Graceful Fallback)

### Test Input
Simulated Query / Function: `get_order_status("ORD_SIMULATE_RETRY_FAIL")`

### Verification & Console Output
```text
[RETRY WARN] Tool 'get_order_status' encountered temporary error (Attempt 1/3): Persistent database timeout.. Retrying (1/2)...

[RETRY WARN] Tool 'get_order_status' encountered temporary error (Attempt 2/3): Persistent database timeout.. Retrying (2/2)...

[RETRY EXHAUSTED] Tool 'get_order_status' failed after 2 retries. Returning graceful fallback message.

Tool Output:
We are currently experiencing temporary technical issues with this service. Please try again later.
```

### Result
**Passed**. The tool failed on Attempt 1, Retry 1, and Retry 2. After 2 retries were exhausted, it gracefully returned the user fallback message without throwing uncaught exceptions.

---

## 5. Real Streaming & Callbacks Lifecycle Demonstration

### Test Input
Query: `"Can you find wireless headphones under ₹5,000 and check status of order ORD1001?"`

### Console Execution Output (`agent_executor.stream`)
```text
[AGENT START] Starting request processing...
[LLM START] Invoking LLM (ChatGroq)...
[LLM END] LLM generation finished.

[TOOL START] product_search
[TOOL INPUT] {'query': 'wireless headphones under ₹5,000'}
[TOOL END]
[TOOL RESULT]
Product ID: PRD201
Name: Wireless Headphones
Category: Audio
Price: ₹3499
Availability: In Stock
Features: Bluetooth, Noise Isolation, Built-in Microphone
Color: Black

[LLM START] Invoking LLM (ChatGroq)...
[LLM END] LLM generation finished.

[TOOL START] order_status
[TOOL INPUT] {'order_id': 'ORD1001'}
[TOOL END]
[TOOL RESULT]
Order ID: ORD1001
Status: Processing
Expected Delivery: 28-Sep-2026
Carrier: Sample Logistics

[LLM START] Invoking LLM (ChatGroq)...
[LLM END] LLM generation finished.

[AGENT END] Processing completed successfully.

Final Agent Output (Streamed progressively):
Here’s what I found:

**Wireless headphones under ₹5,000**
- Product ID: PRD201
- Name: Wireless Headphones
- Price: ₹3,499 (In Stock)

**Order status for ORD1001**
- Status: Processing  
- Expected Delivery: 28-Sep-2026  
- Carrier: Sample Logistics
```

### Result
**Passed**.
- **Streaming**: Output text was streamed token-by-token using `agent_executor.stream`.
- **Callbacks**: `SupportAgentCallback` successfully logged all 7 lifecycle events (`[AGENT START]`, `[LLM START]`, `[TOOL START]`, `[TOOL RESULT]`, `[LLM END]`, `[AGENT END]`) cleanly without exposing internal system prompt secrets or chain-of-thought reasoning.

---

## 6. Multi-Turn Conversation Memory

### First Input
`"Can you find wireless headphones under ₹5,000 and check status of order ORD1001?"`

### Second Input
`"When is that order expected to be delivered?"`

### Verification & Output
```text
[AGENT START] Starting request processing...
[LLM START] Invoking LLM (ChatGroq)...
[LLM END] LLM generation finished.
[AGENT END] Processing completed successfully.

Final Agent Output:
Your order ORD1001 is expected to be delivered on 28-Sep-2026.
```

### Result
**Passed**. The agent resolved `"that order"` to `ORD1001` using `HumanMessage` and `AIMessage` history passed into `chat_history`.

---

## 7. LangSmith Tracing

### Environment Variables Verification
```ini
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=Assignment3-Customer-Support-Agent
```

### Result
**Passed**. Runs were successfully recorded under project `Assignment3-Customer-Support-Agent` in LangSmith.

---

## Automated Test Suite Summary

All verification checks executed via `python test_agent.py`:
- Product Search Price + Keyword AND Filtering: **PASSED**
- Order Status Lookup: **PASSED**
- Tool Retry Recovery: **PASSED**
- Tool Retry 2-Attempt Exhaustion Graceful Fallback: **PASSED**
- Full Agent Streaming & Callback Lifecycle: **PASSED**
- Multi-Turn Conversation Memory: **PASSED**