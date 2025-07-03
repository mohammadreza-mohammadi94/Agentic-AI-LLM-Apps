# /config.py
"""
This module centralizes configuration, keeping it 
separate from the application logic.
"""
import os
from dotenv import load_dotenv

# Load environment variables from the .env file at the start
load_dotenv()

def get_api_key(provider_name: str) -> str:
    """
    Retrieves an API key for a given provider from environment variables.
    Builds the key name (e.g., "OPENAI" -> "OPENAI_API_KEY").
    """
    key_name = f"{provider_name.upper()}_API_KEY"
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in .env file.")
    return api_key

# --- Model Configuration ---
ADVISOR_MODEL = "gpt-4o-mini"
EVALUATOR_MODEL = "gemini-1.5-flash"

# --- Application Settings ---
MAX_RETRIES = 2
