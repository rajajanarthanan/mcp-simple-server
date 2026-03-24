from typing import Annotated, Optional

from pydantic import BaseModel, Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun
from .create_order import CreateActionModel, CreateOperationModel, CreateScheduleModel


class ReplaceOperationModel(BaseModel):
    index: int = Field(
        description="Zero-based operation index to replace in the existing order.",
        ge=0,
    )
    newOperation: CreateOperationModel = Field(
        description="Replacement operation to insert at the given index.",
    )


class ReplaceActionModel(BaseModel):
    operationIndex: int = Field(
        description="Zero-based operation index containing the action to replace.",
        ge=0,
    )
    actionIndex: int = Field(
        description="Zero-based action index to replace within the selected operation.",
        ge=0,
    )
    newAction: CreateActionModel = Field(
        description="Replacement action to insert at the specified position.",
    )


class UpdateOrderRevisionsModel(BaseModel):
    replaceOperations: Optional[list[ReplaceOperationModel]] = Field(
        default=None,
        description="Optional list of operation replacements to apply by index.",
    )
    replaceActions: Optional[list[ReplaceActionModel]] = Field(
        default=None,
        description="Optional list of action replacements to apply by operation and action index.",
    )
    newSchedule: Optional[CreateScheduleModel] = Field(
        default=None,
        description="Optional full replacement schedule when the order timing or plan must be regenerated.",
    )


@mcp.tool(
    name="updateOrder",
    description="Update an existing order by changing its schedule, operations, actions, or metadata.",
)
def update_order(
    userId: Annotated[
        str,
        Field(description="User ID that owns the order being updated.", min_length=1),
    ],
    orderId: Annotated[
        str,
        Field(description="Order ID of the existing order to update.", min_length=1),
    ],
    revisions: Annotated[
        UpdateOrderRevisionsModel,
        Field(description="Requested revisions to apply to the order."),
    ],
    title: Annotated[
        Optional[str],
        Field(description="Optional updated title for the order."),
    ] = None,
    description: Annotated[
        Optional[str],
        Field(description="Optional updated description for the order."),
    ] = None,
) -> dict:
    """Update an existing order and return the result."""
    payload = {
        "userId": userId,
        "orderId": orderId,
        "revisions": revisions.model_dump(exclude_none=True),
        "title": title,
        "description": description,
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    try:
        return call_sup_fun("update-order-tool-function", payload)
    except Exception as exc:
        return {
            "success": False,
            "function": "update-order-tool-function",
            "error": str(exc),
        }
