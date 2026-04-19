"""Claude API wrapper for the summariser."""
import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()


def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Add it to your .env file."
        )
    return anthropic.Anthropic(api_key=api_key)


def summarise(text: str, stream: bool = False) -> dict | None:
    """
    Send text to Claude and return structured summary.
    Returns dict with keys: summary, key_points, action_items, tldr.
    If stream=True, prints tokens live and returns None.
    """
    client = get_client()

    if stream:
        _summarise_stream(client, text)
        return None

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=(
            "You are a precise summariser. "
            "Always respond with ONLY valid JSON — no markdown fences, no preamble. "
            "JSON schema: "
            '{"summary": str, "key_points": [str], "action_items": [str], "tldr": str}'
        ),
        messages=[{"role": "user", "content": f"Summarise this text:\n\n{text}"}],
    )
    raw = message.content[0].text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return raw text wrapped in dict
        return {"summary": raw, "key_points": [], "action_items": [], "tldr": ""}


def _summarise_stream(client: anthropic.Anthropic, text: str) -> None:
    """Stream tokens directly to stdout."""
    print("\n--- Streaming summary ---\n")
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="You are a precise summariser. Return a clear, well-structured summary.",
        messages=[{"role": "user", "content": f"Summarise this text:\n\n{text}"}],
    ) as stream:
        for token in stream.text_stream:
            print(token, end="", flush=True)
    print("\n\n--- End of stream ---\n")
