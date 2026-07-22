def build_prompt(text, tone, audience, formality, length, language="English"):
    """Build a rewrite prompt for the requested output language."""
    return f"""
You are an expert text rewriter.

Rewrite the following text based on:
- Tone: {tone}
- Audience: {audience}
- Formality level: {formality}/10
- Length preference: {length}/10
- Output language: {language}

Guidelines:
- Preserve the original meaning strictly.
- Do not add new facts or remove key information.
- Adjust vocabulary, sentence structure, and clarity.
- Make it appropriate for the specified audience.
- Write the complete rewritten text in {language}.
- Return only the rewritten text; do not add a title, notes, or an explanation.

Source text:
<source_text>
{text}
</source_text>
"""
