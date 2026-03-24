from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


BUSINESS_CONTEXT_ITEM_TYPES = [
	"document",
	"text",
	"image",
	"video",
	"audio",
	"other",
]

BusinessContextItemType = Literal[
	"document",
	"text",
	"image",
	"video",
	"audio",
	"other",
]


class BusinessContextItemModel(BaseModel):
	id: Optional[str] = Field(
		default=None,
		description=(
			"Optional item ID. If provided, the existing item will be updated. "
			"If omitted, a new item is created."
		),
	)
	type: BusinessContextItemType = Field(
		description=f"Type of the context item. Must be one of: {', '.join(BUSINESS_CONTEXT_ITEM_TYPES)}.",
	)
	category: str = Field(
		description=(
			"Category label for the business context item, e.g. 'legal', "
			"'company-profile', 'product-catalog', 'marketing-collateral'."
		),
		min_length=1,
	)
	title: str = Field(
		description="Human-readable title for the item, e.g. 'GST Certificate', 'Company Brochure'.",
		min_length=1,
	)
	description: Optional[str] = Field(
		default=None,
		description="Optional longer description of the item.",
	)
	url: Optional[str] = Field(
		default=None,
		description=(
			"Optional URL associated with the item — can be a link to a document, "
			"image, video, audio, or any other hosted resource."
		),
	)
	content: Optional[str] = Field(
		default=None,
		description="Optional text content of the item (max 10 000 characters).",
	)
	metadata: Optional[dict[str, Any]] = Field(
		default=None,
		description="Optional arbitrary metadata dictionary for extra structured info.",
	)
	isActive: Optional[bool] = Field(
		default=None,
		description="Whether the item is active. Defaults to true on the server side.",
	)


@mcp.tool(
	name="saveUserBusinessContext",
	description=(
		"Save (create or update) a business-context item for the user's business. "
		"Business context includes documents, images, videos, audio, and text related "
		"to the business — e.g. GST certificate, PAN card, company profile, product "
		"catalog, marketing collateral, etc. "
		"If the item includes an id the existing record is updated; otherwise a new "
		"record is inserted. The businessId is resolved server-side from the userId. "
		"Maximum 100 active items per business."
	),
)
def save_user_business_context(
	userId: Annotated[
		str,
		Field(
			description="User ID whose business the context item belongs to.",
			min_length=1,
		),
	],
	item: Annotated[
		BusinessContextItemModel,
		Field(description="Business context item to create or update."),
	],
) -> dict:
	"""Save (create or update) a business context item and return the result."""
	payload = {
		"userId": userId,
		"item": item.model_dump(exclude_none=True),
	}

	try:
		return call_sup_fun("save-user-business-context", payload)
	except Exception as exc:
		return {
			"success": False,
			"function": "save-user-business-context",
			"error": str(exc),
		}

