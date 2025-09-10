"""
Agent creation and execution for the Analytical Chatbot.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain_cohere import create_cohere_react_agent
from src.logger import setup_logger

# Setup Logger
logger = setup_logger()

def create_agent(llm, tools):
    """Create and configure the agent"""
    try:
        prompt = ChatPromptTemplate.from_template("{input}")
        agent = create_cohere_react_agent(
            llm = llm,
            tools = tools,
            prompt = prompt
        )
        agent_executor = AgentExecutor(
            agent = agent,
            tools = tools, 
            verbose=True
        )
        logger.info("Agent and AgentExecutor created successfully.")
        return agent_executor
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise e
    
def run_agent(agent_executor, query):
    """Run the agent with the provided query."""
    try:
        logger.info(f"Processing query: {query}")
        response = agent_executor.invoke({"input": query})
        answer = response.get("output", "No Response Generated...")
        logger.info(f"Agent response: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        raise e