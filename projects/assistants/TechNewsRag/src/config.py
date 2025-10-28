"""
Configuration module for the RAG application.

This module handles the loading of environment variables from a .env file.
It is responsible for ensuring that necessary configurations, such as API keys,
are available for other parts of the application.
"""

import os
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def load_environment():
    """
    Loads environment variables from a .env file.

    This function should be called at the beginning of the application's
    lifecycle to ensure all required environment variables are loaded.
    """
    load_dotenv()
    logger.info("Environment variables loaded from .env file.")
