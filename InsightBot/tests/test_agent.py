"""
Unit tests for agent.
"""
import pytest
from src.llm import initialize_llm
from src.tools import initialize_tools
from src.agent import create_agent
from src.config import Config

def test_create_agent():
    """Test agent creation."""
    Config.MODEL_TYPE = "flan-t5-base"  # Use free model for testing
    llm = initialize_llm()
    tools = initialize_tools()
    agent_executor = create_agent(llm, tools)
    assert agent_executor is not None