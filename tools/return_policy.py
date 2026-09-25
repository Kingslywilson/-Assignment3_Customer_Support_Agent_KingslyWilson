import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from tools.retry_handler import with_tool_retry


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "return_policy.json"
)


def load_return_policy():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["return_policy"]


RETURN_POLICY = load_return_policy()


class ReturnPolicyInput(BaseModel):
    query: str = Field(
        description=(
            "The customer's question about returns, refunds, "
            "return eligibility, charges, damaged products, "
            "or return timelines."
        )
    )


@with_tool_retry(max_retries=2)
def search_return_policy(query: str) -> str:
    if not query or not query.strip():
        return "Error: Return policy query is required."

    query = query.strip().lower()

    matched_keys = set()
    if "return policy" in query or query in {
        "returns",
        "return",
        "refund policy",
        "return and refund policy",
    }:
        matched_keys.update(RETURN_POLICY.keys())
    if any(word in query for word in [
        "how many days",
        "how long",
        "return period",
        "return window",
        "days to return",
        "period"
    ]):
        matched_keys.add("standard_return_period")

    if any(word in query for word in [
        "refund",
        "money back",
        "refund timeline",
        "when will i get"
    ]):
        matched_keys.add("refund_timeline")

    if any(word in query for word in [
        "opened electronics",
        "open electronics",
        "opened electronic",
        "open electronic"
    ]):
        matched_keys.add("opened_electronics")

    if any(word in query for word in [
        "unused product",
        "unused products",
        "condition",
        "accessories"
    ]):
        matched_keys.add("unused_products")

    if any(word in query for word in [
        "return charge",
        "return charges",
        "restocking",
        "fee",
        "fees"
    ]):
        matched_keys.add("return_charges")

    if any(word in query for word in [
        "damaged",
        "damage",
        "arrived damaged"
    ]):
        matched_keys.add("damaged_products")

    if any(word in query for word in [
        "exception",
        "exceptions",
        "excluded",
        "not eligible"
    ]):
        matched_keys.add("exceptions")

    if not matched_keys:
        return f"No return policy information found for: {query}"

    output = []

    for key, value in RETURN_POLICY.items():
        if key in matched_keys:
            formatted_key = key.replace("_", " ").title()
            output.append(f"{formatted_key}: {value}")

    return "\n".join(output)


return_policy_tool = StructuredTool.from_function(
    func=search_return_policy,
    name="return_policy",
    description=(
        "Use this tool for questions about returns, refunds, "
        "return periods, eligibility, damaged products, "
        "return charges, or exceptions. "
        "Only use information from the configured return policy. "
        "Never invent return periods, refund timelines, charges, "
        "exceptions, or eligibility rules."
    ),
    args_schema=ReturnPolicyInput,
)