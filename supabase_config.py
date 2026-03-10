import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def _load_dotenv_file(path: Path) -> dict:
    """Very small .env parser: returns a dict of KEY->VALUE for simple lines.

    Skips comments and blank lines. Does not handle export or complex quoting.
    """
    data = {}
    try:
        text = path.read_text()
    except Exception:
        return data

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        data[k] = v
    return data


def load_supabase_config():
    """Load SUPABASE_URL and SUPABASE_ANON_KEY from env, .env, or sensible defaults.

    Returns:
        (base_url, api_key)
    """
    project_url = os.getenv("SUPABASE_URL")
    api_key = os.getenv("SUPABASE_ANON_KEY")

    if not project_url or not api_key:
        candidate = Path(__file__).resolve().parent
        
        if not candidate.exists():
            candidate = Path(__file__).resolve().parents[1] / ".env"

        if candidate.exists():
            logger.info(f"Loading .env from {candidate}")
            data = _load_dotenv_file(candidate)
            project_url = project_url or data.get("SUPABASE_URL")
            api_key = api_key or data.get("SUPABASE_ANON_KEY")

    if not project_url:
        logger.warning("SUPABASE_URL not found in environment or .env; falling back to http://localhost:54321")
        project_url = "http://localhost:54321"

    if not api_key:
        logger.warning("SUPABASE_ANON_KEY not found in environment or .env; falling back to placeholder key")
        api_key = "my-api-key"

    base_url = f"{project_url.rstrip('/')}/functions/v1"
    return base_url, api_key


# Module-level convenience values
base_url, api_key = load_supabase_config()
