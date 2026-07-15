import difflib
from html import escape

def highlight_differences(original, rewritten):
    """
    Returns HTML string highlighting differences between texts.
    """

    diff = difflib.ndiff(original.split(), rewritten.split())

    result = []

    for word in diff:
        safe_word = escape(word[2:])

        if word.startswith("- "):
            result.append(f"<span style='color:red;text-decoration:line-through;'>{safe_word}</span>")
        elif word.startswith("+ "):
            result.append(f"<span style='color:green;font-weight:bold;'>{safe_word}</span>")
        elif word.startswith("  "):
            result.append(safe_word)

    return " ".join(result)
