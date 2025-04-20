"""
Unit tests for tools.
"""
import pytest
from src.tools import initialize_tools
from src.config import Config

def test_initialize_tools():
    """Test tool initialization."""
    Config.TAVILY_API_KEY = "dummy_key"  # Mock API key
    tools = initialize_tools()
    assert len(tools) == 2
    assert tools[0].name == "internet_search"
    assert tools[1].name == "python_interpreter"