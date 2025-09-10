"""
Logging setup for the Analytical Chatbot project.
"""
import logging
from src.config import Config

def setup_logger():
    """Set up logging configuration."""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)