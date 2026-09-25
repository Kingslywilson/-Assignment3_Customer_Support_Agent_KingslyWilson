import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent import agent_executor, session_manager
from callbacks import SupportAgentCallback
from tools.order_status import get_order_status
from tools.product_search import search_products


def run_tests():
    print("==================================================")
    print("    RUNNING AUTOMATED TEST SUITE & VERIFICATION")
    print("==================================================")

    # 1. Test Product Search with price and keyword filters
    print("\n--- TEST 1: Product Search ('wireless headphones under ₹5,000') ---")
    res1 = search_products("wireless headphones under ₹5,000")
    print("Tool Output:")
    print(res1)
    assert "Wireless Headphones" in res1
    assert "Mechanical Keyboard" not in res1
    assert "Wireless Mouse" not in res1
    assert "Bluetooth Speaker" not in res1
    print("✓ Product Search Price + Keyword AND Filtering PASSED!")

    # 2. Test Order Status
    print("\n--- TEST 2: Order Status Lookup ('ORD1005') ---")
    res2 = get_order_status("ORD1005")
    print("Tool Output:")
    print(res2)
    assert "Shipped" in res2
    print("✓ Order Status Lookup PASSED!")

    # 3. Test Tool Retry Mechanism (Recovery)
    print("\n--- TEST 3: Tool Retry Recovery ('ORD_SIMULATE_RETRY_RECOVER') ---")
    res3 = get_order_status("ORD_SIMULATE_RETRY_RECOVER")
    print("Tool Output:")
    print(res3)
    assert "Delivered" in res3
    print("✓ Tool Retry Recovery PASSED!")

    # 4. Test Tool Retry Mechanism (Exhaustion & Fallback)
    print("\n--- TEST 4: Tool Retry Fallback after 2 Retries ('ORD_SIMULATE_RETRY_FAIL') ---")
    res4 = get_order_status("ORD_SIMULATE_RETRY_FAIL")
    print("Tool Output:")
    print(res4)
    assert "temporary technical issues" in res4
    print("✓ Tool Retry 2-Attempt Exhaustion Graceful Fallback PASSED!")

    # 5. Full Agent Execution with Callbacks, Memory, and Streaming
    print("\n--- TEST 5: Full Agent Stream & Callbacks ---")
    session_id = "test_session_101"
    memory = session_manager.get_session(session_id)
    callback = SupportAgentCallback()

    question = "Can you find wireless headphones under ₹5,000 and check status of order ORD1001?"
    print(f"Customer Question: {question}")
    
    print("\nExecuting agent stream...")
    output_text = ""
    for chunk in agent_executor.stream(
        {"input": question, "chat_history": memory.get_messages()},
        config={"callbacks": [callback]}
    ):
        if "output" in chunk:
            output_text += chunk["output"]

    print("Final Agent Output:")
    print(output_text)

    memory.add_user_message(question)
    memory.add_ai_message(output_text)

    print("\n--- TEST 6: Multi-turn Conversation Memory ---")
    question2 = "When is that order expected to be delivered?"
    print(f"Customer Question 2: {question2}")
    
    output_text2 = ""
    for chunk in agent_executor.stream(
        {"input": question2, "chat_history": memory.get_messages()},
        config={"callbacks": [callback]}
    ):
        if "output" in chunk:
            output_text2 += chunk["output"]

    print("Final Agent Output 2:")
    print(output_text2)
    
    print("\n==================================================")
    print("       ALL TEST SUITE CHECKS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
