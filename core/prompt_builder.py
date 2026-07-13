def build_prompt(text, tone, audience, formality, length):
    """
    Builds a structured prompt for the LLM.

    Parameters:
    - text (str): Input text
    - tone (str): Desired tone
    - audience (str): Target audience
    - formality (int): 1–10
    - length (int): 1–10

    Returns:
    - str: formatted prompt
    """

    prompt = f"""
You are an expert text rewriter.

Rewrite the following text based on:
- Tone: {tone}
- Audience: {audience}
- Formality level: {formality}/10
- Length preference: {length}/10

Guidelines:
- Preserve the original meaning strictly
- Do NOT add new facts or remove key information
- Adjust vocabulary, sentence structure, and clarity
- Make it appropriate for the specified audience

Text:
{text}
"""

    return prompt