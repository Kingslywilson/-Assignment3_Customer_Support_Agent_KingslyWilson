from langchain_core.callbacks import BaseCallbackHandler


class SupportAgentCallback(BaseCallbackHandler):

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown_tool")

        print(f"\n[TOOL START] {tool_name}")
        print(f"[TOOL INPUT] {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"[TOOL RESULT]\n{output}\n")

    def on_tool_error(self, error, **kwargs):
        print(f"[TOOL ERROR] {error}")

    def on_agent_finish(self, finish, **kwargs):
        print("\n[AGENT FINISHED]\n")