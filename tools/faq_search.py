import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from tools.retry_handler import with_tool_retry


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "faq.json"


def load_faqs():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["faqs"]


FAQS = load_faqs()


class FAQSearchInput(BaseModel):
    query: str = Field(
        description="The customer's question or FAQ topic to search for."
    )


@with_tool_retry(max_retries=2)
def search_faq(query: str) -> str:
    if not query or not query.strip():
        return "Error: FAQ search query is required."

    query = query.strip().lower()

    results = []

    for faq in FAQS:
        searchable_text = " ".join(
            [
                faq["topic"],
                faq["question"],
                faq["answer"],
            ]
        ).lower()

        query_words = query.split()

        if query in searchable_text:
            results.append(faq)
            continue

        matching_words = sum(
            1 for word in query_words
            if len(word) > 2 and word in searchable_text
        )

        if matching_words >= 2:
            results.append(faq)

    if not results:
        return f"No FAQ information found for: {query}"

    output = []

    for faq in results:
        output.append(
            f"FAQ ID: {faq['id']}\n"
            f"Topic: {faq['topic']}\n"
            f"Question: {faq['question']}\n"
            f"Answer: {faq['answer']}"
        )

    return "\n\n".join(output)


faq_search_tool = StructuredTool.from_function(
    func=search_faq,
    name="faq_search",
    description=(
        "Search the customer support FAQ information. "
        "Use this tool for general questions about shipping, payment, "
        "order modification, cancellation, warranty, account, or support. "
        "Only return information available in the FAQ data. "
        "Never invent FAQ answers."
    ),
    args_schema=FAQSearchInput,
)