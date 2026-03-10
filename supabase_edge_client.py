import requests
import logging
from supabase_config import base_url, api_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def call_sup_fun(function_name: str, payload: dict):
    """Call a Supabase Edge Function (Functions API v1).

    - function_name: name (or path) of the function (no leading slash required)
    - payload: JSON-serializable body

    Raises requests.RequestException on transport errors and returns parsed JSON on success.
    """
    url = f"{base_url}/{function_name.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        logger.error("Request to Supabase function failed: %s", e)
        raise

    try:
        return res.json()
    except ValueError:
        logger.error("Response from %s was not valid JSON: %s", url, res.text)
        raise
