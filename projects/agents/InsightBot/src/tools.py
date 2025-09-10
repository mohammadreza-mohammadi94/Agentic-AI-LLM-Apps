"""
Tool definitions for the Analytical Chatbot.
"""
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.utilities import PythonREPL
from langchain.agents import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from src.config import Config
from src.logger import setup_logger


logger = setup_logger()

class ToolInput(BaseModel):
    """Schema for PythonREPL tool input."""
    code: str = Field(description="Python code to execute.")


def initialize_tools():
    """Initialize tools for the analytical chatbot."""
    try:
        # Tavily search tool
        tavily_tool = TavilySearchResults(
            max_results = Config.TAVILY_MAX_RESULTS,
            name = "internet_search",
            description = "Route a user query to the internet"
        )
        logger.info("Tavily search tool initialized successfully.")
        
        # PythonREPL Tool
        python_repl = PythonREPL()
        repl_tool = Tool(
            name = "python_interperter",
            description="Executes Python code and returns the result. Runs in a static sandbox, so print or save output.",
            func=python_repl.run,
            args_schema=ToolInput
        )
        logger.info("PythonREPL tool initialized successfully.")
        
        # Return instances 
        return [tavily_tool, repl_tool]
    except Exception as e:
        logger.error(f"Error initializing tools: {e}")
        raise e