from config.settings import MAX_TOKENS
from core.gemini_client import generate_text


def back_translate(text: str, source_language: str = "English") -> str:
    """Translate a rewrite back to neutral English for cross-language validation."""
    return generate_text(
        prompt=f"""
Source language: {source_language}

<rewritten_text>
{text}
</rewritten_text>
""",
        system_instruction=(
            "You are a precise translator and editor. Translate the supplied rewritten text "
            "into neutral English. If it is already in English, produce a neutral English "
            "restatement instead. Preserve every fact, qualifier, and intended meaning. "
            "Return only the English back-translation, with no labels or commentary."
        ),
        temperature=0.2,
        max_tokens=MAX_TOKENS,
    )
