import json
import re
from difflib import SequenceMatcher

from core.gemini_client import generate_text


def similarity_score(text1: str, text2: str) -> float:
    """Return a lightweight lexical fallback score."""
    if not text1.strip() or not text2.strip():
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def semantic_similarity_score(original_text: str, back_translated_text: str) -> float:
    """Score semantic preservation after back-translation on a 0-1 scale."""
    if not original_text.strip() or not back_translated_text.strip():
        return 0.0

    response = generate_text(
        prompt=f"""
Compare the meaning of the original text and its English back-translation.
Give a semantic similarity score from 0.0 to 1.0, where 1.0 means every fact,
qualification, and intent is preserved, and 0.0 means the meaning is unrelated.

Original text:
<original>
{original_text}
</original>

English back-translation:
<back_translation>
{back_translated_text}
</back_translation>
""",
        system_instruction=(
            "You are a strict semantic-equivalence evaluator. Assess meaning, not wording. "
            "Return only valid JSON in exactly this shape: {\"score\": 0.0}."
        ),
        temperature=0.0,
        max_tokens=80,
    )

    return _extract_similarity_score(response)


def _extract_similarity_score(response: str) -> float:
    """Parse an evaluator response while tolerating Markdown code fences."""
    cleaned_response = response.strip()
    if cleaned_response.startswith("```"):
        cleaned_response = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned_response)

    try:
        score = float(json.loads(cleaned_response)["score"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("The semantic similarity evaluator returned an invalid score.") from exc

    return max(0.0, min(1.0, score))


def meaning_drift(score: float, threshold: float = 0.80) -> bool:
    return score < threshold
