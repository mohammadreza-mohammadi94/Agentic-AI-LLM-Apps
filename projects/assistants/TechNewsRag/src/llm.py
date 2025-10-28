"""
LLM Module

This module is responsible for initializing and configuring the language model (LLM).
It provides a function to get a chat model instance, which can be used for
generating responses in the RAG chain.
"""

import os
import logging
from langchain_openai import ChatOpenAI

# Setup logging
logger = logging.getLogger(__name__)

def get_chat_model(
    model_name: str = "gpt-4o-mini", temperature: float = 0.0, max_tokens: int = 500
) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI model instance.

    Parameters
    ----------
    model_name: str
        Name of the OpenAI model to use
    temperature: float
        Temperature setting for response generation
    max_tokens: int
        Maximum tokens in the response

    Returns
    -------
    ChatOpenAI
        Configured ChatOpenAI model instance

    Raises
    ------
    ValueError
        If OPENAI_API_KEY environment variable is not set
    """
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI API KEY Not found...")

    model = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    logger.info(f"Chat model loaded: {model_name}")
    return model