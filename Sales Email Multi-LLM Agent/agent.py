# -*- coding: utf-8 -*-
"""
multi_agent_sdr_system.py

This script implements a hierarchical multi-agent system to automate the
process of drafting, refining, and sending personalized sales emails. The system
leverages multiple LLM providers and a robust guardrail system to ensure
safe and effective operation.

Architecture Overview:
- A top-level "Sales Manager" agent orchestrates the entire workflow.
- Three specialist "Writer" agents, each powered by a different LLM provider
  (DeepSeek, Google Gemini, Groq), generate email drafts with unique personas.
- An "Input Guardrail" uses a dedicated agent to check user prompts for
  personal names, preventing potential privacy issues.
- A sub-system "Email Manager" agent handles the final steps of formatting
  (subject line, HTML conversion) and sending the chosen email.
"""

# --- 1. Imports and Initial Setup ---
import os
import asyncio
from typing import Dict, List
from dotenv import load_dotenv
from pprint import pprint

# Pydantic is used for creating structured data models.
from pydantic import BaseModel, Field

# The official OpenAI Agents SDK library.
# To install: pip install openai-agents
from agents import (
    Agent,
    Runner,
    trace,
    function_tool,
    OpenAIChatCompletionsModel,
    input_guardrail,
    GuardrailFunctionOutput,
)
from openai import AsyncOpenAI


# --- 2. Configuration and Environment Loading ---
import os
import sys

REQUIRED_KEYS = [
    'OPENAI_API_KEY',
    'GOOGLE_API_KEY',
    'DEEPSEEK_API_KEY',
    'GROQ_API_KEY',
    'SENDGRID_API_KEY'
]

def validate_env():
    print("🔍 Validating environment...")

    # بررسی وجود فایل .env
    if not os.path.isfile(".env"):
        print("❌ Error: .env file not found in the current directory.")
        print("   Current Directory:", os.getcwd())
        print("   Files in directory:", os.listdir())
        sys.exit(1)

    # بررسی بارگذاری کلیدها
    missing_keys = [key for key in REQUIRED_KEYS if not os.getenv(key)]
    if missing_keys:
        print("❌ Error: The following required environment variables are missing:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n💡 Make sure your `.env` file is correctly formatted, like:")
        print("   OPENAI_API_KEY=sk-...")
        print("   (no quotes, no spaces)")
        sys.exit(1)

    print("✅ Environment validated successfully.\n")


print("Loading environment variables...")
load_dotenv(override=True)

# Load API keys from the .env file
# It's crucial to have these set for the script to function.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

validate_env()

# Check if essential keys are loaded
if not all([OPENAI_API_KEY, GOOGLE_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY, SENDGRID_API_KEY]):
    print("Warning: Not all API keys are set in the .env file. The script may fail.")


# --- 3. Multi-Provider LLM Setup ---

# Define base URLs for different OpenAI-compatible LLM providers.
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Initialize asynchronous clients for each provider.
deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=DEEPSEEK_API_KEY)
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=GOOGLE_API_KEY)
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
# It doesn't need a base_url as it defaults to OpenAI's servers.
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Create model instances by wrapping each client.
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)
gemini_model = OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=gemini_client)
llama3_model = OpenAIChatCompletionsModel(model="llama3-70b-8192", openai_client=groq_client)

# FIX: Pass the newly created openai_client to the model definition.
gpt4o_mini_model = OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=openai_client)

# --- 4. Guardrail Definition ---

class NameCheckOutput(BaseModel):
    """Pydantic model for the guardrail's structured output."""
    is_name_in_message: bool = Field(description="True if a personal name is found, otherwise False.")
    name: str = Field(description="The personal name that was found, or an empty string if none.")

# A dedicated agent whose only job is to check for personal names.
guardrail_agent = Agent(
    name="Name_Check_Agent",
    instructions="Check if the user's message includes a person's first or last name (e.g., Alice, Bob, Smith). A job title like 'CEO' or a role like 'Head of Business Development' is not a personal name.",
    output_type=NameCheckOutput,
    model=gpt4o_mini_model
)


@input_guardrail
async def guardrail_against_personal_names(agent_input, *args, **kwargs) -> GuardrailFunctionOutput:
    """
    Input guardrail that uses a dedicated agent to detect personal names.
    """
    # استخراج پیام واقعی از context
    user_message = agent_input.context.input_messages[0].content

    print(f"🕵️  INPUT GUARDRAIL: Checking message for personal names: '{user_message}'")

    # اجرای agent گاردریل
    result = await Runner.run(guardrail_agent, user_message)

    if result.is_name_in_message:
        print(f"🚨 GUARDRAIL TRIPPED: Personal name '{result.name}' found in input.")
        return GuardrailFunctionOutput(
            fail=True,
            message=f"Input rejected by guardrail: Found personal name '{result.name}'.",
            tripwire_triggered=True
        )
    else:
        print("✅ GUARDRAIL PASSED: No personal names found.")
        return GuardrailFunctionOutput()



# --- 5. Tool and Agent System Initialization ---

def initialize_agent_system() -> Agent:
    """
    Initializes and assembles the complete hierarchical multi-agent system.

    This function defines all specialist agents, converts them into tools,
    and constructs the manager agent that orchestrates the entire workflow.
    It returns the top-level Sales Manager agent, ready for execution.
    """
    
    # --- Define Specialist "Worker" Agents ---
    # Each agent has a specific persona and uses a different underlying model.
    professional_writer_agent = Agent(name="Professional_Writer", instructions="Write a professional, serious cold email.", model=deepseek_model)
    engaging_writer_agent = Agent(name="Engaging_Writer", instructions="Write a witty, engaging cold email.", model=gemini_model)
    concise_writer_agent = Agent(name="Concise_Writer", instructions="Write a concise, to-the-point cold email.", model=llama3_model)
    
    # --- Convert Writer Agents into Tools for the Manager ---
    professional_tool = professional_writer_agent.as_tool(tool_name="professional_writer", tool_description="Writes an email in a professional and serious tone.")
    engaging_tool = engaging_writer_agent.as_tool(tool_name="engaging_writer", tool_description="Writes an email in a witty and engaging tone.")
    concise_tool = concise_writer_agent.as_tool(tool_name="concise_writer", tool_description="Writes an email in a concise and direct tone.")
    
    # --- Define the Top-Level Orchestrator Agent ---
    # This agent manages the entire process from start to finish.
    sales_manager_instructions = """
    You are a sales manager. Your goal is to generate the most effective cold sales email.
    1. Use all three writer tools (professional_writer, engaging_writer, concise_writer) to generate three different versions of the email based on the user's request.
    2. Analyze the three versions and select the single best one that you believe will be most effective.
    3. Output ONLY the final, chosen email body. Do not add any extra text or explanation.
    """
    
    sales_manager = Agent(
        name="Sales_Manager",
        instructions=sales_manager_instructions,
        tools=[professional_tool, engaging_tool, concise_tool],
        model=gpt4o_mini_model,
        # The guardrail is attached here to protect this agent's inputs.
        input_guardrails=[guardrail_against_personal_names]
    )
    
    return sales_manager


# --- 6. Main Execution Logic ---
async def main():
    """
    The main entry point for running and testing the agent system.
    This function demonstrates two test cases: one that triggers the guardrail
    and one that passes, showcasing the system's safety features.
    """
    print("Initializing agent system...")
    sales_manager_agent = initialize_agent_system()
    
    # --- Test Case 1: This message contains a personal name and WILL trigger the guardrail ---
    print("\n--- 🛑 Test Case 1: Running with input that should FAIL the guardrail 🛑 ---")
    message_with_name = "Send a cold sales email to the CEO of a fast-growing startup, from Alice."
    
    try:
        with trace("SDR_Workflow_Guardrail_FAIL"):
            # FIX: Changed back to Runner.run
            await Runner.run(sales_manager_agent, message_with_name)
    except Exception as e:
        # We expect a GuardrailTripwireTriggered exception here.
        print(f"\n✅ SUCCESS: The process was correctly stopped by the guardrail.")
        print(f"   Error: {e}\n")

    # --- Test Case 2: This message uses a job title and WILL PASS the guardrail ---
    print("\n\n--- ✅ Test Case 2: Running with input that should PASS the guardrail ✅ ---")
    message_without_name = "Send a cold sales email to the CEO of a fast-growing startup, from the Head of Business Development."
    
    try:
        with trace("SDR_Workflow_Guardrail_PASS"):
            # FIX: Changed back to Runner.run
            result = await Runner.run(sales_manager_agent, message_without_name)
            print("\n🏁 Workflow Finished Successfully. Final chosen email:")
            pprint(result)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: The process failed unexpectedly: {e}")

if __name__ == "__main__":
    asyncio.run(main())