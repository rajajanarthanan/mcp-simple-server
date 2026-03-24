from typing import Annotated, Optional

from pydantic import Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


@mcp.tool(
    name="createSupportTicket",
    description="Create a support ticket when the user needs help beyond automated resolution.",
)
def create_support_ticket(
    source: Annotated[
        str,
        Field(
            description="Ticket source channel (for example: mcp, app, chatbot).",
            min_length=1,
        ),
    ],
    title: Annotated[
        str,
        Field(description="Short title/summary for the support issue.", min_length=1),
    ],
    severity: Annotated[
        Optional[str],
        Field(description="Optional severity level (for example: low, medium, high)."),
    ] = None,
    detail: Annotated[
        Optional[str],
        Field(description="Optional detailed description of the issue."),
    ] = None,
    userId: Annotated[
        Optional[str],
        Field(description="Optional user ID related to the ticket."),
    ] = None,
    actionId: Annotated[
        Optional[str],
        Field(description="Optional action ID for traceability."),
    ] = None,
    orderId: Annotated[
        Optional[str],
        Field(description="Optional order ID linked to the issue."),
    ] = None,
    operationId: Annotated[
        Optional[str],
        Field(description="Optional operation ID linked to the issue."),
    ] = None,
) -> dict:
    """Raise a support ticket with the provided context and return the ticket result."""
    payload = {
        "source": source,
        "title": title,
        "severity": severity,
        "detail": detail,
        "userId": userId,
        "actionId": actionId,
        "orderId": orderId,
        "operationId": operationId,
    }

    # Match the edge function contract: omit unset optional fields.
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        result = call_sup_fun("create-support-ticket-tool-function", payload)
        return result
    except Exception as exc:
        return {
            "success": False,
            "function": "create-support-ticket-tool-function",
            "error": str(exc),
        }
