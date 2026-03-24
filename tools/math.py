from typing import Annotated

from pydantic import Field

from app.mcp_app import mcp


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


@mcp.tool(
    name="multiply",
    description="Multiply two numbers and return the product.",
)
def multiply(
    a: Annotated[float, Field(description="First factor to multiply")],
    b: Annotated[float, Field(description="Second factor to multiply")],
) -> float:
    """Use this tool when the user asks to multiply numeric values."""
    return a * b

