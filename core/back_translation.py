from config.settings import MAX_TOKENS
from core.gemini_client import generate_text


def back_translate(text: str):
    """
    Converts rewritten text back into a neutral version
    so that it can be compared with the original.
    """

    return generate_text(
        prompt=text,
        system_instruction=(
            "You are an expert editor. Rewrite the given text into a completely neutral tone "
            "without changing its meaning."
        ),
        temperature=0.2,
        max_tokens=MAX_TOKENS,
    )
