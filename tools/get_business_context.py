from typing import Annotated, Optional

from pydantic import Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun

from .save_business_context import BusinessContextItemType


@mcp.tool(
	name="getUserBusinessContext",
	description=(
		"Retrieve active business-context items for the user's business. "
		"Business context includes documents, images, videos, audio, and text related "
		"to the business — e.g. GST certificate, PAN card, company profile, product "
		"catalog, marketing collateral, etc. "
		"Results can be filtered by type and/or category. "
		"The businessId is resolved server-side from the userId."
	),
)
def get_user_business_context(
	userId: Annotated[
		str,
		Field(
			description="User ID whose business context items should be retrieved.",
			min_length=1,
		),
	],
	type: Annotated[
		Optional[BusinessContextItemType],
		Field(
			description="Optional filter by item type (document, text, image, video, audio, other).",
		),
	] = None,
	category: Annotated[
		Optional[str],
		Field(
			description=(
				"Optional filter by category label, e.g. 'legal', "
				"'company-profile', 'product-catalog', 'marketing-collateral'."
			),
		),
	] = None,
) -> dict:
	"""Fetch active business context items, optionally filtered by type and category."""
	payload: dict = {"userId": userId}

	if type is not None:
		payload["type"] = type
	if category is not None:
		payload["category"] = category

	try:
		return call_sup_fun("get-user-business-context", payload)
	except Exception as exc:
		return {
			"success": False,
			"function": "get-user-business-context",
			"error": str(exc),
		}

