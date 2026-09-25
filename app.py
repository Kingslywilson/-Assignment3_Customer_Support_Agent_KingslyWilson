import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent import agent_executor, session_manager
from callbacks import SupportAgentCallback


def ask_agent(session_id: str, question: str) -> str:
    memory = session_manager.get_session(session_id)
    chat_history = memory.get_messages()

    callback = SupportAgentCallback()

    final_answer = ""

    # Execute stream progressively
    for chunk in agent_executor.stream(
        {
            "input": question,
            "chat_history": chat_history,
        },
        config={"callbacks": [callback]},
    ):
        if "output" in chunk:
            text_chunk = chunk["output"]
            print(text_chunk, end="", flush=True)
            final_answer += text_chunk

    print()

    # Save to session memory
    memory.add_user_message(question)
    memory.add_ai_message(final_answer)

    return final_answer


def main():
    print("=" * 60)
    print("       AUTONOMOUS CUSTOMER SUPPORT AGENT")
    print("=" * 60)
    print("Type 'exit' to quit.")
    print()

    session_id = input("Session ID: ").strip()

    if not session_id:
        session_id = "default"

    print(f"\nSession started: {session_id}")
    print("You can ask about orders, products, FAQs, returns, and refunds.")
    print()

    while True:
        question = input("Customer: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("\nThank you for contacting customer support.")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        try:
            print("\nAgent: ", end="", flush=True)
            ask_agent(session_id, question)
            print()

        except Exception as error:
            print("\nAgent Error:")
            print("Sorry, I was unable to process your request.")
            print(f"Details: {error}")
            print()


if __name__ == "__main__":
    main()