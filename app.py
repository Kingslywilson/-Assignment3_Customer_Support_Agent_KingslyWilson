from agent import agent_executor, session_manager
from callbacks import SupportAgentCallback


def ask_agent(session_id: str, question: str):
    memory = session_manager.get_session(session_id)

    history = "\n".join(
        f"{message.type}: {message.content}"
        for message in memory.get_messages()
    )

    if history:
        agent_input = (
            f"Previous conversation:\n{history}\n\n"
            f"Current customer question:\n{question}"
        )
    else:
        agent_input = question

    memory.add_user_message(question)

    callback = SupportAgentCallback()

    response = agent_executor.invoke(
        {"input": agent_input},
        config={"callbacks": [callback]},
    )

    answer = response["output"]

    memory.add_ai_message(answer)

    return answer


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
            answer = ask_agent(session_id, question)

            print("\nAgent:")
            print(answer)
            print()

        except Exception as error:
            print("\nAgent Error:")
            print("Sorry, I was unable to process your request.")
            print(f"Details: {error}")
            print()


if __name__ == "__main__":
    main()