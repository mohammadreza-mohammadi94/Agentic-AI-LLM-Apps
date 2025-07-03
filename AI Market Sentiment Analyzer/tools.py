"""
Defines the tools the agent can use and their 
corresponding Python functions.
"""
# /tools.py

import os
import json
from config import OUTPUT_DIR

# --- Tool Implementation ---
def save_market_insights(report_content, filename):
    """
    Saves the market research report content to a file.

    Args:
        report_content (str): The detailed market analysis and strategy.
        filename (str): The suggested filename for the report (e.g., "strategy_report.txt").

    Returns:
        str: A confirmation message indicating the result of the operation.
    """

    try:
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Sanitize filename to prevent directory traversal issues
        safe_filename = os.path.basename(filename)
        filepath = os.path.join(OUTPUT_DIR, safe_filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        return f"Successfully saved the report to {filepath}"
    except Exception as e:
        return f"Error saving file: {e}"


# --- Tool Definitions for the LLM ---
def get_tool_definitions() -> list[dict]:
    """
    Returns the JSON schema definitions for all available tools.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "save_market_insights",
                "description": "Saves a detailed market research report, including analysis and strategy, to a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_content": {
                            "type": "string",
                            "description": "The full text of the market research report to be saved."
                        },
                        "filename": {
                            "type": "string",
                            "description": "A descriptive filename for the report, e.g., 'company_x_strategy.md'."
                        }
                    },
                    "required": ["report_content", "filename"]
                }
            }
        }
    ]

# --- Tool Dispatcher ---

AVAILABLE_TOOLS = {
    "save_market_insights": save_market_insights,
}