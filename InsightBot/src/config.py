"""
Configuration settings for the Analytical Chatbot project.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for project.
    """
    """Configuration class for project settings."""
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    LOG_FILE = "agent.log"
    OUTPUT_DIR = "outputs"
    MODEL_TYPE = "cohere"  # or "flan-t5-base" for free model
    MAX_SEARCH_RESULTS = 3

    @staticmethod
    def validate():
        """
        Validate the configuration settings.
        """
        if not Config.COHERE_API_KEY and Config.MODEL_TYPE == "cohere":
            raise ValueError("Cohere API key is required for Cohere model.")
        if not Config.TAVILY_API_KEY:
            raise ValueError("Tavily API key is required for Tavily API.")
        
    @staticmethod
    def setup_output_dir():
        """Creats output directory for storing results."""
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        print(f"Output directory '{Config.OUTPUT_DIR}' is ready for use.")


