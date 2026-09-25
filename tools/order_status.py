import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from tools.retry_handler import with_tool_retry


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def load_orders():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["orders"]


ORDERS = load_orders()

_SIMULATED_FAILURE_ATTEMPTS = {}


class OrderStatusInput(BaseModel):
    order_id: str = Field(
        description="The customer order ID, for example ORD1005"
    )


@with_tool_retry(max_retries=2)
def get_order_status(order_id: str) -> str:
    if isinstance(order_id, dict):
        order_id = order_id.get("order_id", "")

    if not order_id or not order_id.strip():
        return "Error: Order ID is required."

    order_id = order_id.strip().upper()

    # Simulated retry recovery test mode
    if "RETRY_RECOVER" in order_id:
        _SIMULATED_FAILURE_ATTEMPTS[order_id] = _SIMULATED_FAILURE_ATTEMPTS.get(order_id, 0) + 1
        if _SIMULATED_FAILURE_ATTEMPTS[order_id] == 1:
            raise RuntimeError("Temporary network failure connecting to order database.")
        return "Order ID: ORD1005\nStatus: Delivered\nExpected Delivery: 2026-09-20\nCarrier: FedEx"

    # Simulated retry exhaustion test mode
    if "RETRY_FAIL" in order_id:
        raise RuntimeError("Persistent database timeout.")

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