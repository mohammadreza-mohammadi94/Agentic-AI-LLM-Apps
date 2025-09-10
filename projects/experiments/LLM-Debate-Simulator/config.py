import os
from dotenv import load_dotenv


def load_api_key(provider_name):
    """
    Loads an API key for a given provider from environment variables.

    This function first loads the .env file and then attempts to retrieve
    the specified API key. It raises a ValueError if the key is not found.

    Args:
        provider_name (str): The name of the LLM provider (e.g., "OPENAI", "GROQ").

    Returns:
        str: The API key.

    Raises:
        ValueError: If the API key is not found in the environment variables.
    """
    # Load environment variables from a .env file
    load_dotenv()

    api_key_name = f"{provider_name.upper()}"
    api_key = os.getenv(api_key_name)

    if not api_key:
        raise ValueError(f"Error: {api_key_name} not found in .env file. Please add it to your .env file.")
    
    return api_key


# Constants
DEBATE_TOPIC = "Should remote work be the default standard for all tech companies?"
RESULTS_DIR = "results"
RANKED_DEBATE_FILE = os.path.join(RESULTS_DIR, "ranked_debate.json")
DEBATE_SUMMARY_FILE = os.path.join(RESULTS_DIR, "debate_summary.md")