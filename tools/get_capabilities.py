from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


@mcp.tool(
    name="getCapabilities",
    description="Get the list of available capabilities the assistant can use.",
)
def get_capabilities() -> dict:
    """Return the available capabilities to help plan what actions can be performed."""
    try:
        result = call_sup_fun("get-capabilities-tool-function", {})
        return result
    except Exception as exc:
        return {
            "success": False,
            "function": "get-capabilities-tool-function",
            "error": str(exc),
        }
