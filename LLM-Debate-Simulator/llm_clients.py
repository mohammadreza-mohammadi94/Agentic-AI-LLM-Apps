# /llm_clients.py
"""
This module manages communication with various APIs and provides a 
uniform interface for sending requests to different models.
"""

import openai
import groq
from config import load_api_key

# Initialize clients once to reuse connections
# This is more efficient than creating a new client for every call.
try:
    openai_client = openai.OpenAI(api_key=load_api_key("OPENAI_API_KEY"))
    groq_client = groq.Groq(api_key=load_api_key("GROQ_API_KEY"))
except ValueError as e:
    print(e)
    # You might want to exit or handle this more gracefully
    openai_client = None
    groq_client = None

# A dictionary mapping providers to their respective clients
CLIENTS = {
    'openai': openai_client,
    'groq': groq_client
}

def query_llm(provider, model, prompt, is_json=False):
    """
    Queries a specified LLM from a given provider.

    Args:
        provider (str): The LLM provider (e.g., 'openai', 'groq').
        model (str): The model name (e.g., 'gpt-4o-mini', 'llama3-8b-8192').
        prompt (str): The prompt to send to the model.
        is_json (bool): Whether to enable JSON mode for the response (if supported).

    Returns:
        str: The content of the LLM's response.

    Raises:
        ValueError: If the provider is not supported.
        Exception: For API-related errors.
    """
    client = CLIENTS.get(provider.lower())
    if not client:
        raise ValueError(f"Unsupported provider: {provider}. Supported: {list(CLIENTS.keys())}")
    
    try:
        # Prepare arguments for the API call
        chat_completion_args = {
            "model": model,
            "messages": [
                {"role": "system",
                 "content": prompt}
                        ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        # Enable JSON mode if requested and provider is OpenAI
        if is_json and provider.lower() == "openai":
            chat_completion_args['response_format'] = {"type": "json_object"}

        # Make the API Call
        response = client.chat.completions.create(**chat_completion_args)
        content = response.choices[0].message.content

        return content.strip() if content else ""
    except Exception as e:
        print(f"An error occured while querying {provider}/{model}: {e}")
        # Return an empty string or re-raise the exception
        return f"Error: Could not get a response from {model}"
    
