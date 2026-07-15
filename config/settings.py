import os

SIMILARITY_THRESHOLD = 0.80
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
MAX_TOKENS = 500
TEMPERATURE = 0.7
