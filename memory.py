from langchain_core.messages import HumanMessage, AIMessage


class ConversationMemory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, message: str):
        self.messages.append(HumanMessage(content=message))

    def add_ai_message(self, message: str):
        self.messages.append(AIMessage(content=message))

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()