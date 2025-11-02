"""
Central configuration file for the ArxivHybridSearch project.

This module defines constants for paths, model names, and logging settings
to ensure consistency and ease of maintenance across the application.
"""

import logging
from pathlib import Path

# --- Path Configuration ---
# This setup ensures that paths are relative to the project root,
# regardless of where the script is executed from.
try:
    # Get the directory of the current script (e.g., .../src)
    SRC_DIR = Path(__file__).resolve().parent
    # Get the project root directory (one level up from 'src')
    PROJECT_ROOT = SRC_DIR.parent
except NameError:
    # Fallback for interactive environments like Jupyter
    PROJECT_ROOT = Path.cwd()

# Define absolute paths for data and the vector store
DOCS_PATH = PROJECT_ROOT / "docs"
VECTOR_STORE_PATH = PROJECT_ROOT / "faiss_db"

# --- Model Configurations ---
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
LLM_MODEL_NAME = "gpt-3.5-turbo"

# --- Logging Configuration ---
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """Configures the root logger for the application."""
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
    )
