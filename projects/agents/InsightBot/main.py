"""
Main entry point for the Analytical Chatbot project.
"""
from src.config import Config
from src.llm import initialize_llm
from src.tools import initialize_tools
from src.agent import create_agent
from src.ui import run_ui
from src.logger import setup_logger

def main():
    """Run the Analytical Chatbot."""
    logger = setup_logger()
    logger.info("Starting Analytical Chatbot...")

    try:
        # Validate config and setup
        Config.validate()
        Config.setup_output_dir()

        # Initialize components
        llm = initialize_llm()
        tools = initialize_tools()
        agent_executor = create_agent(llm, tools)

        # Run Streamlit UI
        run_ui(agent_executor)
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

if __name__ == "__main__":
    main()