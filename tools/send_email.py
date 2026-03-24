from typing import Annotated, Optional

from pydantic import BaseModel, Field

from app.mcp_app import mcp
from supabase_edge_client import call_sup_fun


class AttachmentModel(BaseModel):
	url: str = Field(
		description="Public URL of the attachment file.",
		min_length=1,
	)
	filename: str = Field(
		description="File name to use for the attachment (e.g. 'report.pdf').",
		min_length=1,
	)


@mcp.tool(
	name="sendEmail",
	description="Send a transactional email on behalf of the AI Agent.",
)
def send_email(
	to: Annotated[
		str,
		Field(
			description="Recipient email address.",
			min_length=1,
		),
	],
	subject: Annotated[
		str,
		Field(
			description="Email subject line.",
			min_length=1,
		),
	],
	body: Annotated[
		str,
		Field(
			description="Email body content (plain text or HTML).",
			min_length=1,
		),
	],
	attachments: Annotated[
		Optional[list[AttachmentModel]],
		Field(
			description="Optional list of attachments, each with a url and filename.",
		),
	] = None,
) -> dict:
	"""Send a transactional email and return the result."""
	payload = {
		"to": to,
		"subject": subject,
		"body": body,
	}

	if attachments is not None:
		payload["attachments"] = [a.model_dump() for a in attachments]

	try:
		return call_sup_fun("send-email", payload)
	except Exception as exc:
		return {
			"success": False,
			"function": "send-email",
			"error": str(exc),
		}
