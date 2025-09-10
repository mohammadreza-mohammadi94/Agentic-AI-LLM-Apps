# utils.py
from pathlib import Path

def load_prompt(path: Path, text: str) -> str:
    """
    Loads a prompt template from a file and replaces a placeholder with text.

    Args:
        path (Path): The path to the prompt template file.
        text (str): The text to insert into the "{TEXT}" placeholder.

    Returns:
        str: The formatted prompt with the text injected.
    """
    template = path.read_text(encoding="utf-8")
    return template.replace("{TEXT}", text)