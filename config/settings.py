import os

SIMILARITY_THRESHOLD = 0.80
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
MAX_TOKENS = 500
TEMPERATURE = 0.7

# English is deliberately first: Streamlit uses the first selectbox option by default.
SUPPORTED_LANGUAGES = (
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Dutch",
    "Russian",
    "Arabic",
    "Hindi",
    "Bengali",
    "Tamil",
    "Telugu",
    "Japanese",
    "Korean",
    "Chinese (Simplified)",
    "Vietnamese",
    "Indonesian",
    "Turkish",
)
