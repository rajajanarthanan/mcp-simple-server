from typing import Annotated

from pydantic import Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


@mcp.tool(
    name="getOrderInfo",
    description="Get complete information about an order, including schedule, operations, actions, and results.",
)
def get_order_info(
    orderId: Annotated[
        str,
        Field(description="Order ID for which full order context is required.", min_length=1),
    ],
) -> dict:
    """Return full order context for the provided order ID."""
    try:
        return call_sup_fun("get-order-info-tool-function", {"orderId": orderId})
    except Exception as exc:
        return {
            "success": False,
            "function": "get-order-info-tool-function",
            "error": str(exc),
        }
