import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


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
            "category, feature, price limit, or availability."
        )
    )


def search_products(query: str) -> str:
    if not query or not query.strip():
        return "Error: Product search query is required."

    query = query.strip().lower()

    results = []

    # Extract a simple "under price" condition
    max_price = None

    words = query.replace(",", "").split()

    for i, word in enumerate(words):
        if word.isdigit() and i > 0 and words[i - 1] in {
            "under",
            "below",
            "less",
            "than"
        }:
            max_price = int(word)

    for product in PRODUCTS:
        searchable_text = " ".join(
            [
                product["name"],
                product["category"],
                product["description"],
                product["availability"],
                product["color"],
                *product["features"],
            ]
        ).lower()

        matches_query = query in searchable_text

        matches_price = (
            max_price is not None
            and product["price"] < max_price
        )

        if matches_query or matches_price:
            results.append(product)

    if not results:
        return f"No products found for: {query}"

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