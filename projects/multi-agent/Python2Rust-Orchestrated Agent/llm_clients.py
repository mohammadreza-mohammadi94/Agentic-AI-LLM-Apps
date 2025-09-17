# Imports
import os
from typing import List, Any
from groq import Groq
from cerebras.cloud.sdk import Cerebras
from config import MODEL_CONFIG

def _stream_and_collect(stream):
    """Helper function to collect text from a streaming API response."""
    reply = ""
    for chunk in stream:
        fragment = chunk.choices[0].delta.content or "" 
        reply += fragment
        print(fragment, end="", flush=True)
    return reply.strip()


# Grog client class
class GroqClient:
    """Client for interacting with models on the Groq platform."""
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Grog API KEY not found.")
        self.client = Groq(api_key=api_key)
    
    def generate(self, model_name: str, messages: List[Any]) -> str:
        """Generates a response from a Groq model."""
        config = MODEL_CONFIG["groq"]["models"][model_name]
        stream = self.client.chat.completions.create(
            messages=messages,
            model=model_name,
            stream=True,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            top_p=config["top_p"]
        )
        return _stream_and_collect(stream)


class CerebrasClient:
    """Client for interacting with models on the Cerebras Platform."""
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Cerebras API KEY not found.")
        self.client = Cerebras(api_key=api_key)

    def generate(self, model_name: str, messages: List[Any]) -> str:
        """Generates a response from a Cerebras model."""
        config = MODEL_CONFIG["cerebras"]["models"][model_name]
        stream = self.client.chat.completions.create(
            messages=messages,
            model=model_name,
            stream=True,
            max_completion_tokens=config['max_tokens'],
            temperature=config['temperature'],
            top_p=config['top_p']
        )

        return _stream_and_collect(stream)
