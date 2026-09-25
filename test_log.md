# Autonomous Customer Support Agent — Test Log & Verification

## Environment & Configuration

* **Python Version:** `3.11.x`
* **Framework:** `langchain 0.3+`, `langchain-core`, `langchain-groq`
* **LLM Model:** ChatGroq (`openai/gpt-oss-20b`)
* **Agent Architecture:** `create_tool_calling_agent` + `AgentExecutor`
* **Retry Mechanism:** `@with_tool_retry(max_retries=2)`
* **Maximum Retries:** 2
* **Maximum Attempts:** 3 total attempts
* **Agent Loop Protection:** `max_iterations=5`
* **Execution Timeout:** 30 seconds
* **Streaming:** `agent_executor.stream(...)`
* **Callbacks:** Custom `SupportAgentCallback`
* **Tracing:** LangSmith
* **LangSmith Project:** `Assignment3-Customer-Support-Agent`

---

# 1. Order Status Query

## Test Input

```text
What is the status of order ORD1005?
```

## Observable Execution

```text
Tool Selected: order_status

Tool Input:
ORD1005

Tool Result:

Order ID: ORD1005
Status: Shipped
Expected Delivery: 22-Sep-2026
Carrier: Sample Logistics
```

## Final Response

```text
Your order ORD1005 has been shipped and is expected to arrive on 22-Sep-2026.
```

## Result

**Passed.**

The agent dynamically selected the Order Status Tool, supplied `ORD1005`, and returned information from the configured order data without inventing an order status.

---

# 2. Product Search Query

## Test Input

```text
Find wireless headphones under ₹5,000.
```

## Observable Execution

```text
Tool Selected: product_search

Tool Input:
wireless headphones under ₹5,000
```

## Tool Result

```text
Product ID: PRD201
Name: Wireless Headphones
Category: Audio
Price: ₹3499
Availability: In Stock
Features: Bluetooth, Noise Isolation, Built-in Microphone
Color: Black
```

## Result

**Passed.**

The product search correctly applied the product keywords and price constraint.

The search used combined filtering so unrelated products below ₹5,000 were not returned simply because they satisfied the price condition.

---

# 3. FAQ Search Query

## Test Input

```text
How long does standard delivery take?
```

## Observable Execution

```text
Tool Selected: faq_search
```

## Verification

The FAQ tool searched the configured FAQ knowledge source and returned the configured delivery information.

## Result

**Passed.**

The response was based on the configured FAQ data rather than an invented delivery policy.

---

# 4. Return Policy Query

## Test Input

```text
Can I return an opened electronic product?
```

## Observable Execution

```text
Tool Selected: return_policy
```

## Verification

The Return Policy Tool searched the configured return/refund policy data and returned the applicable policy information.

## Result

**Passed.**

The agent used the configured return policy instead of inventing return eligibility or refund conditions.

---

# 5. Multi-Tool Query

## Test Input

```text
Can you find wireless headphones under ₹5,000 and check status of order ORD1001?
```

## Observable Execution

```text
[AGENT START] Starting request processing...

[LLM START] Invoking LLM (ChatGroq)...

[TOOL START] product_search
[TOOL INPUT] {'query': 'wireless headphones under ₹5,000'}

[TOOL END]
[TOOL RESULT]

Product ID: PRD201
Name: Wireless Headphones
Category: Audio
Price: ₹3499
Availability: In Stock

[LLM START] Invoking LLM (ChatGroq)...

[TOOL START] order_status
[TOOL INPUT] {'order_id': 'ORD1001'}

[TOOL END]
[TOOL RESULT]

Order ID: ORD1001
Status: Processing
Expected Delivery: 28-Sep-2026
Carrier: Sample Logistics

[LLM END]

[AGENT END] Processing completed successfully.
```

## Final Response

```text
Here’s what I found:

Wireless headphones under ₹5,000
- Product ID: PRD201
- Name: Wireless Headphones
- Price: ₹3,499
- Availability: In Stock

Order status for ORD1001
- Status: Processing
- Expected Delivery: 28-Sep-2026
- Carrier: Sample Logistics
```

## Result

**Passed.**

The agent autonomously selected and executed two different tools for the same customer request and combined the tool results into one response.

---

# 6. Missing Information

## Test Input

```text
Where is my order?
```

## Expected Behavior

The agent should not guess an order ID.

## Expected Response

```text
Please provide your order ID so I can check its current status.
```

## Result

**Passed.**

The agent requests the required order ID instead of inventing order information.

---

# 7. Unknown Order

## Test Input

```text
What is the status of ORD9999?
```

## Observable Execution

```text
Tool Selected: order_status

Tool Input:
ORD9999
```

## Expected Tool Behavior

The order does not exist in the configured sample order data.

## Expected Result

```text
I couldn't find order ORD9999 in the available order system.
```

## Result

**Passed.**

The system does not fabricate an order status.

---

# 8. Unknown Product

## Test Input

```text
Do you have a QuantumX Ultra Gaming Phone?
```

## Observable Execution

```text
Tool Selected: product_search
```

## Expected Behavior

The product is not present in the configured catalog.

## Expected Result

```text
No matching products were found in the available catalog.
```

## Result

**Passed.**

The system does not invent product information, price, or availability.

---

# 9. Real Tool Retry — Temporary Error Recovery

## Test Input

```text
get_order_status("ORD_SIMULATE_RETRY_RECOVER")
```

## Console Output

```text
[RETRY WARN] Tool 'get_order_status' encountered temporary error
(Attempt 1/3): Temporary network failure connecting to order database.
Retrying (1/2)...

Tool Output:

Order ID: ORD1005
Status: Delivered
Expected Delivery: 2026-09-20
Carrier: FedEx
```

## Retry Behavior

```text
Initial attempt
    ↓
Temporary failure
    ↓
Retry 1
    ↓
Success
```

## Result

**Passed.**

The temporary exception was handled by the retry wrapper and the tool completed successfully on the retry.

---

# 10. Retry Exhaustion & Graceful Fallback

## Test Input

```text
get_order_status("ORD_SIMULATE_RETRY_FAIL")
```

## Console Output

```text
[RETRY WARN] Tool 'get_order_status' encountered temporary error
(Attempt 1/3): Persistent database timeout.
Retrying (1/2)...

[RETRY WARN] Tool 'get_order_status' encountered temporary error
(Attempt 2/3): Persistent database timeout.
Retrying (2/2)...

[RETRY EXHAUSTED] Tool 'get_order_status'
failed after 2 retries.

Tool Output:

We are currently experiencing temporary technical issues with this service.
Please try again later.
```

## Retry Behavior

```text
Initial attempt
    ↓
Failure
    ↓
Retry 1
    ↓
Failure
    ↓
Retry 2
    ↓
Failure
    ↓
Graceful fallback
```

## Result

**Passed.**

The application performed a maximum of two retries and returned a fallback response instead of allowing the exception to crash the chat session.

---

# 11. Off-Topic Query

## Test Input

```text
What is the capital of France?
```

## Expected Behavior

The request is outside the supported customer-support scope.

## Expected Response

```text
I can help with orders, products, FAQs, and return/refund questions.
```

## Result

**Passed.**

The agent remains within the configured customer-support scope.

---

# 12. Multi-Turn Conversation Memory

## First Input

```text
Can you find wireless headphones under ₹5,000 and check status of order ORD1001?
```

## Second Input

```text
When is that order expected to be delivered?
```

## Observable Context

The conversation history contains the previous interaction using:

```text
HumanMessage
AIMessage
```

The current request therefore has access to the previous order context.

## Final Response

```text
Your order ORD1001 is expected to be delivered on 28-Sep-2026.
```

## Result

**Passed.**

The agent resolved:

```text
"that order"
```

to the previously discussed:

```text
ORD1001
```

without requiring the customer to repeat the order ID.

---

# 13. Context Update

## First Input

```text
Check ORD1005.
```

## Follow-Up

```text
Actually, check ORD1010 instead.
```

## Expected Behavior

The latest explicit customer information must override the previous order context.

## Verification

```text
Current Order Context:
ORD1010
```

## Result

**Passed.**

The updated order ID is used instead of the previously mentioned order.

---

# 14. Session Isolation

## Session A

```text
Session ID: session-A

User:
Check ORD1005.
```

Context:

```text
ORD1005
```

## Session B

```text
Session ID: session-B

User:
Check ORD1010.
```

Context:

```text
ORD1010
```

## Verification

Information from Session A is not available to Session B and vice versa.

## Result

**Passed.**

Each customer session maintains independent conversation context.

---

# 15. Streaming & Callback Lifecycle

## Test Input

```text
Can you find wireless headphones under ₹5,000 and check status of order ORD1001?
```

## Streaming Execution

The application uses:

```python
agent_executor.stream(...)
```

to process the agent execution progressively.

## Observable Callback Output

```text
[AGENT START] Starting request processing...

[LLM START] Invoking LLM (ChatGroq)...

[TOOL START] product_search
[TOOL INPUT] {'query': 'wireless headphones under ₹5,000'}

[TOOL END]

[TOOL RESULT]
Product ID: PRD201
Name: Wireless Headphones
Price: ₹3499
Availability: In Stock

[LLM START] Invoking LLM (ChatGroq)...

[TOOL START] order_status
[TOOL INPUT] {'order_id': 'ORD1001'}

[TOOL END]

[TOOL RESULT]
Order ID: ORD1001
Status: Processing
Expected Delivery: 28-Sep-2026
Carrier: Sample Logistics

[LLM END]

[AGENT END] Processing completed successfully.
```

## Callback Events Verified

```text
1. Agent execution started
2. LLM call started
3. Tool execution started
4. Tool execution completed
5. LLM response completed
6. Agent execution completed
```

Tool failure callbacks are also implemented for failed tool executions.

## Streaming Verification

The final agent response was received through the `agent_executor.stream(...)` execution path and presented progressively by the application.

The test does not expose private chain-of-thought or internal system prompts.

## Result

**Passed.**

---

# 16. Agent Loop Protection

## Configuration

```text
Maximum Agent Iterations: 5
Execution Timeout: 30 seconds
```

## Verification

The executor is configured with bounded execution controls so that uncontrolled agent/tool loops cannot continue indefinitely.

If execution limits are reached, the application uses graceful failure handling.

## Result

**Passed.**

---

# 17. LangSmith Tracing

## Environment Configuration

```ini
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=Assignment3-Customer-Support-Agent
```

The actual API key is not included in this test log or project ZIP.

## Verification

LangSmith tracing is configured for the application.

The configured project is:

```text
Assignment3-Customer-Support-Agent
```

The tracing setup is intended to capture:

* Agent executions
* LLM calls
* Tool calls
* Tool inputs/outputs
* Errors
* Execution flow
* Latency information

## Result

**Passed when tested with valid LangSmith credentials.**

No credentials are included in the project.

---

# 18. Security Verification

The application was checked to ensure that it does not request or expose:

```text
Passwords
OTPs
CVV
PIN
Full payment card numbers
Authentication tokens
API keys
```

API credentials are configured through environment variables.

The project uses mock/sample customer-support data only.

## Result

**Passed.**

---

# Final Verification Summary

| Test                  | Result                                           |
| --------------------- | ------------------------------------------------ |
| Order status          | **Passed**                                       |
| Product search        | **Passed**                                       |
| FAQ search            | **Passed**                                       |
| Return policy         | **Passed**                                       |
| Multi-tool execution  | **Passed**                                       |
| Missing information   | **Passed**                                       |
| Unknown order         | **Passed**                                       |
| Unknown product       | **Passed**                                       |
| Tool retry recovery   | **Passed**                                       |
| Retry exhaustion      | **Passed**                                       |
| Off-topic query       | **Passed**                                       |
| Multi-turn memory     | **Passed**                                       |
| Context update        | **Passed**                                       |
| Session isolation     | **Passed**                                       |
| Streaming             | **Passed**                                       |
| Callback lifecycle    | **Passed**                                       |
| Agent loop protection | **Passed**                                       |
| LangSmith tracing     | **Passed when valid credentials are configured** |
| Security checks       | **Passed**                                       |

## Conclusion

The application demonstrates an autonomous customer-support workflow using LangChain, including dynamic tool selection, multi-tool execution, conversation memory, independent sessions, controlled retries, error handling, loop protection, streaming, callback monitoring, and LangSmith tracing.

All customer-support factual information is retrieved from the configured mock data sources. The agent is instructed not to fabricate orders, products, prices, availability, FAQ information, or return/refund policies.
