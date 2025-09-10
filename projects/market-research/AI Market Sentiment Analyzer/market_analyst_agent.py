"""
This is the core orchestrator for the agent.
"""
# /market_analyst_agent.py

import openai
import json
from config import OPENAI_API_KEY, ANALYSIS_MODEL
from prompts import get_system_prompt
from tools import get_tool_definitions, AVAILABLE_TOOLS

class MarketAnalystAgent:
    """
    An agent that analyzes website content and uses tools to report findings.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def analyze(self, news_content: str, topic: str):
        """
        Performs analysis on the news content and handles tool calls.
        """
        system_prompt = get_system_prompt(topic)
        tool_definitions = get_tool_definitions()
        
        print("🤖 Agent: Analyzing news content and formulating strategy...")
        
        response = self.client.chat.completions.create(
            model=ANALYSIS_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                # FIX: Use 'news_content' instead of 'website_content'
                {"role": "user", "content": news_content}
            ],
            tools=tool_definitions,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            self._handle_tool_calls(response_message.tool_calls)
        else:
            print("🤖 Agent: The model did not use any tools. Here is the response:")
            print(response_message.content)

    def _handle_tool_calls(self, tool_calls):
        """
        Executes the tool calls requested by the model.
        """
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = AVAILABLE_TOOLS.get(function_name)
            
            if not function_to_call:
                print(f"Error: Model tried to call an unknown function: {function_name}")
                continue

            try:
                function_args = json.loads(tool_call.function.arguments)
                print(f"🤖 Agent: Calling tool `{function_name}` with arguments: {function_args}")
                
                function_response = function_to_call(**function_args)
                print(f"✅ Tool Response: {function_response}")

            except json.JSONDecodeError:
                print(f"Error: Could not decode arguments for function {function_name}.")
            except TypeError as e:
                print(f"Error: Invalid arguments for function {function_name}: {e}")