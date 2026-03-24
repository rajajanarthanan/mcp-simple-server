from typing import Annotated

from pydantic import Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


@mcp.tool(
    name="getCapabilitiesPricing",
    description="Calculate total credits required for a list of capabilities.",
)
def get_capabilities_pricing(
    capabilityIds: Annotated[
        list[str],
        Field(
            description="List of capability IDs to price. Duplicates increase total credits.",
            min_length=1,
        ),
    ],
) -> dict:
    """Return total credits for the provided capabilities."""
    try:
        return call_sup_fun(
            "get-capabilities-pricing-tool-function",
            {"capabilityIds": capabilityIds},
        )
    except Exception as exc:
        return {
            "success": False,
            "function": "get-capabilities-pricing-tool-function",
            "error": str(exc),
        }
