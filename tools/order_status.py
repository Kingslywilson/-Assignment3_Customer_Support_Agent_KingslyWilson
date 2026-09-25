import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


# Load order data
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def load_orders():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["orders"]


ORDERS = load_orders()


class OrderStatusInput(BaseModel):
    order_id: str = Field(
        description="The customer order ID, for example ORD1005"
    )


def get_order_status(order_id: str) -> str:
    if isinstance(order_id, dict):
        order_id = order_id.get("order_id", "")

    if not order_id or not order_id.strip():
        return "Error: Order ID is required."

    order_id = order_id.strip().upper()

    if not order_id.startswith("ORD"):
        return "Error: Invalid order ID format. Order ID should start with ORD."

    for order in ORDERS:
        if order["order_id"] == order_id:
            return (
                f"Order ID: {order['order_id']}\n"
                f"Status: {order['status']}\n"
                f"Expected Delivery: {order['expected_delivery'] or 'Not available'}\n"
                f"Carrier: {order['carrier'] or 'Not available'}"
            )

    return f"Order {order_id} was not found."


order_status_tool = StructuredTool.from_function(
    func=get_order_status,
    name="order_status",
    description=(
        "Use this tool to check the status of a customer order. "
        "Requires a valid order ID such as ORD1005. "
        "Never guess or invent order information."
    ),
    args_schema=OrderStatusInput,
)