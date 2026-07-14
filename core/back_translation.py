from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def back_translate(text: str):
    """
    Converts rewritten text back into a neutral version
    so that it can be compared with the original.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert editor. "
                    "Rewrite the given text into a completely neutral tone "
                    "without changing its meaning."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content