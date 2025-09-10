import os
import openai
from dotenv import load_dotenv

def get_openai_client():
    """
    Initializes and returns the OpenAI client, loading the API key from .env.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or environment variables.")
    
    return openai.OpenAI(api_key=api_key)
