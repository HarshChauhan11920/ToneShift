from difflib import SequenceMatcher


def similarity_score(text1: str, text2: str) -> float:
    if not text1.strip() or not text2.strip():
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def meaning_drift(score: float, threshold: float = 0.80):
    return score < threshold
