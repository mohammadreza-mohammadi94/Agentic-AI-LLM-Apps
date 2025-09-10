# /llm_client.py
"""
This module abstracts away the specifics of each LLM's API.
"""

import openai
import google.generativeai as genai
from config import get_api_key, ADVISOR_MODEL, EVALUATOR_MODEL

# Configure clients globally
try:
    openai_client = openai.OpenAI(api_key=get_api_key("OPENAI"))
    genai.configure(api_key=get_api_key("GOOGLE"))
    gemini_client = genai.GenerativeModel(EVALUATOR_MODEL)
except ValueError as e:
    # This will print the "key not found" error once on startup if keys are missing
    print(e)
    openai_client = None
    gemini_client = None

def query_advisor(prompt: str) -> str:
    """Queries the advisor LLM (OpenAI)."""
    if not openai_client:
        return "Error: OpenAI API key is not configured. Please check your .env file."
    try:
        response = openai_client.chat.completions.create(
            model=ADVISOR_MODEL,
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content or "No response from advisor."
    except Exception as e:
        return f"An error occurred while querying OpenAI: {e}"

def query_evaluator(prompt: str) -> str:
    """Queries the evaluator LLM (Gemini)."""
    if not gemini_client:
        return "ACCEPT: Evaluator API key is not configured. Skipping evaluation."
    try:
        response = gemini_client.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Fail open (ACCEPT) to avoid blocking the user if the evaluator has an issue
        return f"ACCEPT: An error occurred during evaluation: {e}"