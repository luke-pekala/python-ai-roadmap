"""Prompt templates for the summariser."""

SYSTEM_JSON = (
    "You are a precise summariser. "
    "Always respond with ONLY valid JSON — no markdown fences, no preamble. "
    'JSON schema: {"summary": str, "key_points": [str], "action_items": [str], "tldr": str}'
)

SYSTEM_PLAIN = (
    "You are a precise summariser. "
    "Return a clean, well-structured plain-text summary."
)

def build_user_prompt(text: str) -> str:
    return f"Summarise this text:\n\n{text}"
