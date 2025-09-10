"""
Streamlit UI for the Analytical Chatbot.
"""
import streamlit as st
import os
from src.config import Config
from src.logger import setup_logger

logger = setup_logger()

def run_ui(agent_executor):
    """Run the Streamlit UI."""
    st.header("Analytical Chatbot 💬")
    st.sidebar.title("Analytical Chatbot")
    st.sidebar.markdown(
        """
        This chatbot uses LangChain, Cohere (or flan-t5-base), and Tavily Search to answer questions and create visualizations.
        - Built with [Streamlit](https://streamlit.io/)
        - Powered by [LangChain](https://python.langchain.com/)
        """
    )

    query = st.text_input("Ask a question (e.g., 'Plot employees of top 3 tech companies 2024' or 'What is the capital of France?')")
    if query:
        try:
            answer = agent_executor.invoke({"input": query})
            st.write("**Answer:**")
            st.write(answer.get("output", "No response generated"))

            # Check for plot output
            plot_path = os.path.join(Config.OUTPUT_DIR, "plot.png")
            if os.path.exists(plot_path):
                st.image(plot_path, caption="Generated Plot")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"UI error: {str(e)}")