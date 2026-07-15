import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.settings import MODEL_NAME

load_dotenv()


def generate_text(
    prompt: str,
    system_instruction: str,
    temperature: float,
    max_tokens: int,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add your Gemini API key to the .env file before running the app."
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response. Try a shorter input or a different model.")

    return response.text.strip()
