import os
import anthropic
from dotenv import load_dotenv


def make_client():
    """Anthropic client. Reads ANTHROPIC_API_KEY from the environment, loading
    .env first so a local key file works without exporting anything."""
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set -- add it to your environment or a .env file."
        )
    return anthropic.Anthropic(api_key=api_key)
