# utils.py
from pathlib import Path

def load_prompt(path: Path, replacements: dict) -> str:
    """
    Loads a prompt template from a file and replaces placeholders with provided values.

    This function allows for multiple placeholders in the format {key}.

    Args:
        path (Path): The path to the prompt template file.
        replacements (dict): A dictionary where keys are the placeholder names
                             (without brackets) and values are the text to insert.

    Returns:
        str: The formatted prompt with all placeholders replaced.
    
    Example:
        # If prompt file contains: "Hello, {name}! Your issue is: {issue}."
        # Call with: load_prompt(path, {"name": "Ali", "issue": "Login problem"})
        # Returns: "Hello, Ali! Your issue is: Login problem."
    """
    template = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace(f"{{{key}}}", str(value))
    return template