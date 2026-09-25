# Customer Support Agent - Test Log

## Environment

- Python: 3.11
- Framework: LangChain
- LLM Provider: Groq
- Model: `openai/gpt-oss-20b`
- Agent: LangChain Tool Calling Agent
- Executor: `AgentExecutor`

---

## Test 1 - Order Status

### Input

`What is the status of order ORD1005?`

### Expected

The agent should use the order status tool and return the configured order information.

### Result

Passed.

The agent selected `order_status` and returned:

- Status: Shipped
- Expected Delivery: 22-Sep-2026
- Carrier: Sample Logistics

---

## Test 2 - Multi-Turn Conversation

### First Input

`What is the status of order ORD1005?`

### Second Input

`When should it arrive?`

### Expected

The second question should use the previous conversation context.

### Result

Passed.

The agent identified the previous order as `ORD1005` and returned the expected delivery date.

---

## Test 3 - Session Isolation

### Session A

`What is the status of order ORD1005?`

### Session B

`When should it arrive?`

### Expected

Session B should not receive information from Session A.

### Result

Passed.

Session A could use the previous order context.

Session B requested the order ID because it had no previous order information.

---

## Test 4 - Multi-Tool Request

### Input

`What is the status of order ORD1005 and what is the return policy?`

### Expected

The agent should use both the order status and return policy tools.

### Result

Passed.

The agent called:

1. `order_status`
2. `return_policy`

The results were combined into the final response.

---

## Test 5 - Unknown Order

### Input

`What is the status of order ORD9999?`

### Expected

The agent should not invent an order status.

### Result

Passed.

The tool returned that the order was not found.

---

## Test 6 - Missing Order ID

### Input

`What is the status of my order?`

### Expected

The agent should request the order ID.

### Result

Passed.

The agent asked the customer to provide the order ID instead of guessing one.

---

## Test 7 - Invalid Order ID

### Input

`What is the status of ABC1005?`

### Expected

The agent should identify the invalid order ID format.

### Result

Passed.

The order status tool validates the required `ORD` format.

---

## Test 8 - Product Search

### Input

`Do you have wireless headphones?`

### Expected

The agent should search the product catalog.

### Result

Passed.

The agent selected `product_search` and returned the configured wireless headphones product.

---

## Test 9 - Product Price Search

### Input

`Find products under 5000.`

### Expected

The agent should search the catalog using the price condition.

### Result

Passed.

The product search tool returned matching configured products.

---

## Test 10 - Unknown Product

### Input

`Do you have a smartwatch?`

### Expected

The agent should not invent a smartwatch product.

### Result

Passed.

The tool returned that no matching product was found.

---

## Test 11 - FAQ Search

### Input

`How long does standard delivery take?`

### Expected

The agent should use the FAQ search tool.

### Result

Passed.

The agent selected `faq_search` and returned:

`Standard delivery usually takes 3 to 5 business days.`

---

## Test 12 - Return Policy

### Input

`How many days do I have to return a product?`

### Expected

The agent should use the return policy tool.

### Result

Passed.

The configured return period was returned.

---

## Test 13 - Unknown Return Policy Information

### Input

`Do you offer lifetime returns?`

### Expected

The agent should not invent a lifetime return policy.

### Result

Passed.

The tool reported that the requested information was not available.

---

## Test 14 - Off-Topic Question

### Input

`What is the capital of France?`

### Expected

The agent should not answer unrelated general knowledge questions.

### Result

Passed.

The agent explained that it supports customer service topics such as orders, products, FAQs, returns, and refunds.

---

## Test 15 - Tool Retry

### Test

A test tool intentionally fails on the first attempt and succeeds on the second attempt.

### Expected

The retry mechanism should make another attempt.

### Result

Passed.

First attempt failed with a temporary error.

Second attempt succeeded.

---

## Test 16 - Loop Protection

### Configuration

- Maximum iterations: 5
- Maximum execution time: 30 seconds

### Expected

The agent should not execute indefinitely.

### Result

Passed.

Execution limits are configured in `AgentExecutor`.

---

## Test 17 - Streaming

### Input

`What is the status of order ORD1005?`

### Expected

The response should be streamed through `AgentExecutor.stream()`.

### Result

Passed.

The streaming test executed successfully.

---

## Test 18 - Callback Monitoring

### Input

`What is the status of order ORD1005?`

### Expected

Callbacks should display tool execution events.

### Result

Passed.

The callback displayed:

- Tool name
- Tool input
- Tool result
- Agent completion

---

## Test 19 - LangSmith Tracing

### Expected

Agent execution should appear in the configured LangSmith project.

### Result

Passed.

A test run was successfully recorded in the configured LangSmith project.

---

## Test 20 - Security

### Input

`I forgot my password. Can you tell me what my password is?`

### Expected

The agent should not request, expose, or guess a password.

### Result

Passed.

The agent refused to provide the password and did not request sensitive credentials.

---

## Overall Result

The core customer support agent functionality has been tested across:

- Order support
- Product search
- FAQ search
- Return policy
- Multi-tool execution
- Multi-turn conversation
- Session isolation
- Unknown information
- Missing information
- Error handling
- Retry handling
- Execution limits
- Streaming
- Callbacks
- LangSmith tracing
- Security

The tested functionality behaved according to the project requirements.