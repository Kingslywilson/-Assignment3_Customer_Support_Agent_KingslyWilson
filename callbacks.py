from typing import Any, Dict, List, Optional
from langchain_core.callbacks import BaseCallbackHandler


class SupportAgentCallback(BaseCallbackHandler):

    def on_chain_start(
        self, serialized: Optional[Dict[str, Any]], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        if kwargs.get("parent_run_id") is None:
            print("\n[AGENT START] Starting request processing...")

    def on_llm_start(
        self, serialized: Optional[Dict[str, Any]], prompts: List[str], **kwargs: Any
    ) -> None:
        serialized_dict = serialized or {}
        model_name = serialized_dict.get("name") or "ChatGroq"
        print(f"[LLM START] Invoking LLM ({model_name})...")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        print("[LLM END] LLM generation finished.")

    def on_tool_start(
        self, serialized: Optional[Dict[str, Any]], input_str: str, **kwargs: Any
    ) -> None:
        serialized_dict = serialized or {}
        tool_name = serialized_dict.get("name", "unknown_tool")
        print(f"\n[TOOL START] {tool_name}")
        print(f"[TOOL INPUT] {input_str}")

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        print("[TOOL END]")
        print(f"[TOOL RESULT]\n{output}\n")

    def on_tool_error(
        self, error: BaseException, **kwargs: Any
    ) -> None:
        print(f"[TOOL ERROR] {error}")

    def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
        print("\n[AGENT END] Processing completed successfully.\n")