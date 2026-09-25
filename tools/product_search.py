import json
import re
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from tools.retry_handler import with_tool_retry


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"


def load_products():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["products"]


PRODUCTS = load_products()


class ProductSearchInput(BaseModel):
    query: str = Field(
        description=(
            "Product search query. Can contain a product name, "
            "category, feature, price limit, color, or availability."
        )
    )


@with_tool_retry(max_retries=2)
def search_products(query: str) -> str:
    if not query or not query.strip():
        return "Error: Product search query is required."

    raw_query = query.strip()
    query_lower = raw_query.lower()

    max_price = None

    price_match = re.search(r'(?:under|below|less than|max|up to|<|rs\.?|₹)\s*(\d[\d,.]*)', query_lower)
    if price_match:
        try:
            val_str = price_match.group(1).replace(",", "")
            max_price = float(val_str)
        except ValueError:
            pass

    if max_price is None:
        words = query_lower.replace(",", "").split()
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\d.]', '', word)
            if clean_word.isdigit() and i > 0 and words[i - 1] in {"under", "below", "less", "than", "<", "max"}:
                max_price = float(clean_word)
                break

    clean_query = re.sub(r'(?:under|below|less than|max|up to|above|more than|>|<|rs\.?|₹)\s*(\d[\d,.]*)', '', query_lower)
    clean_query = re.sub(r'\b(?:under|below|less|than|max|rs|rupees|in|for|with|show|me|find|get|products?|items?|available|price|priced|search)\b', ' ', clean_query)
    keywords = [kw for kw in clean_query.split() if len(kw) > 1]

    results = []

    for product in PRODUCTS:
        if max_price is not None and product["price"] > max_price:
            continue
        searchable_fields = [
            product["name"],
            product["category"],
            product["description"],
            product["availability"],
            product["color"],
            *product["features"],
        ]
        searchable_text = " ".join(searchable_fields).lower()

        if keywords:
            matches_all = True
            for kw in keywords:
                if kw not in searchable_text:
                    matches_all = False
                    break
            if not matches_all:
                continue

        results.append(product)

    if not results:
        return f"No products found matching: '{raw_query}'"

    output = []
    for product in results:
        output.append(
            f"Product ID: {product['product_id']}\n"
            f"Name: {product['name']}\n"
            f"Category: {product['category']}\n"
            f"Price: ₹{product['price']}\n"
            f"Availability: {product['availability']}\n"
            f"Features: {', '.join(product['features'])}\n"
            f"Color: {product['color']}"
        )

    return "\n\n".join(output)


product_search_tool = StructuredTool.from_function(
    func=search_products,
    name="product_search",
    description=(
        "Search the product catalog using product names, categories, "
        "features, prices, colors, or availability. "
        "Use this tool when the customer asks to find or compare products. "
        "Never invent products, prices, features, or stock information."
    ),
    args_schema=ProductSearchInput,
)