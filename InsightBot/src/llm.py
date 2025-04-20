"""
Language model initialization for the Analytical Chatbot.
"""
from langchain_cohere import ChatCohere
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from src.config import Config
from src.logger import setup_logger

# Set logger
logger = setup_logger()

def initialize_llm():
    """Initialize the language model based on config."""
    try:
        if Config.MODEL_TYPE == 'cohere':
            llm = ChatCohere()
            logger.info("Cohere LLM Initialized Successfully")
        elif Config.MODEL_TYPE == 'flan-t5-base':
            pipe = pipeline(
                task = "text2text-generation",
                model = "google/flan-t5-base",
                max_length = 512,
                temperature = 0.7,
                top_p = 0.9,
            )
            llm = HuggingFacePipeline(pipeline=pipe)
            logger.info("HuggingFace LLM Initialized Successfully")
        else:
            raise ValueError(f"Unsupported model type: {Config.MODEL_TYPE}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise e
    

