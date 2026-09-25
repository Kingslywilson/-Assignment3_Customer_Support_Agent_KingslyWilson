from memory import ConversationMemory


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str) -> ConversationMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationMemory()

        return self.sessions[session_id]

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id].clear()

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]