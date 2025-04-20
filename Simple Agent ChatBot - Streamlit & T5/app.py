"""
Simple Agent Chat: A Streamlit-based chatbot that uses a LangChain Agent with a free Hugging Face model (flan-t5-base) and Tavily Search to answer user questions, either directly or by searching the web.

Author: Mohammadreza Mohammadi
Github: mohamamdreza-mohammadi94
"""

#----------------------------------#
# Import Libraries & Setup Project #
#----------------------------------#

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Setup API
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file. Please set it.")
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

# Setup logging
LOG_FILE = "agent.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Save logs to file
        logging.StreamHandler()         # Show logs in console
    ]
)
logger = logging.getLogger(__name__)

#------------------------------#
# Implement App and Streamlit  #
#------------------------------#
def main():
    logger.info("Starting the Agent Chat App...")
    st.header("Agent Chat 💬")
    st.sidebar.title("LangChain Agent ChatBot")
    st.sidebar.markdown(
        '''
        This is an LLM-powered Agent chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [Hugging Face](https://huggingface.co/) flan-t5-base LLM
        - [Tavily Search](https://tavily.com/) for web search
        '''
    )

    # Initialize LLM
    try:
        # Use free Hugging Face model (flan-t5-base)
        pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=512,
            temperature=0.7,
            top_p=0.9
        )
        llm = HuggingFacePipeline(pipeline=pipe)
        logger.info("flan-t5-base LLM initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        st.error(f"Error initializing LLM: {str(e)}")
        return

    # Initialize Tools
    tools = [
        TavilySearchResults(max_results=3, name="tavily_search")
    ]
    logger.info("Tavily Search tool initialized")

    # Define Prompt Template
    prompt = ChatPromptTemplate.from_template(
                """
                You are a helpful assistant with access to the following tools:
                {tools}
                The tools available are: {tool_names}
                Use the tools to answer the user's question as accurately as possible. If you don't have enough information, say so.
                Question: {input}
                {agent_scratchpad}
                """
)

    # Create Agent
    try:
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        logger.info("Agent and AgentExecutor created successfully")
    except Exception as e:
        logger.error(f"Error creating Agent: {str(e)}")
        st.error(f"Error creating Agent: {str(e)}")
        return

    # User Input
    query = st.text_input("Ask a Question (e.g., 'What is the capital of France?' or 'Latest tech news 2025')")
    if query:
        logger.info(f"User query: {query}")
        try:
            # Run Agent
            response = agent_executor.invoke(
                {"input": query},
                config={"callbacks": [st.write]}  # Stream output to Streamlit
            )
            answer = response.get("output", "No response generated")
            st.write("**Answer:**")
            st.write(answer)
            logger.info(f"Response generated: {answer}")
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            st.error(f"An Error Occurred: {str(e)}")

if __name__ == '__main__':
    main()