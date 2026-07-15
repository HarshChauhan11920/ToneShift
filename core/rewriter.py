from config.settings import MAX_TOKENS, TEMPERATURE
from core.gemini_client import generate_text


def rewrite_text(prompt: str):
    """
    Sends the prompt to Gemini and returns the rewritten text.
    """

    return generate_text(
        prompt=prompt,
        system_instruction="You are an expert writing assistant. Rewrite text while preserving its meaning.",
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
