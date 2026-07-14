from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def similarity_score(text1: str, text2: str):
    """
    Returns cosine similarity between two texts.
    """

    embeddings = model.encode([text1, text2])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)

def meaning_drift(score: float, threshold: float = 0.80):
    """
    Determines whether the rewritten text
    has drifted too far from the original meaning.
    """

    return score < threshold