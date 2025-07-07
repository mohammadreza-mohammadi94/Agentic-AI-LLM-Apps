# -*- coding: utf-8 -*-
"""
sales_email_automation.py

This script implements a hierarchical multi-agent system to automate the
process of drafting, refining, and sending sales emails. The system leverages
the openai-agents SDK to create a team of specialized AI agents that
collaborate under the direction of a manager agent.

Architecture Overview:
- A top-level "Sales Manager" agent orchestrates the entire workflow.
- Three specialist "Writer" agents generate email drafts with different personas.
- A sub-system "Email Manager" agent handles the final steps of formatting
  and sending the email, using its own team of specialist tools.
"""

# --- 1. Imports and Initial Setup ---
import os
import asyncio
from typing import Dict
from dotenv import load_dotenv
from pprint import pprint

# The official OpenAI Agents SDK library
# To install: pip install openai-agents
from openai_agents import Agent, run, track, function_tool


# --- 2. Configuration and Environment Loading ---

# Load environment variables from a .env file (e.g., API keys)
load_dotenv(override=True)


# --- 3. Agent Instructions (Defined as Constants) ---

# Instructions are defined as constants for better readability and maintenance.
PROFESSIONAL_INSTRUCTIONS = """
You are a sales agent working for ComplAI, a company that provides a SaaS tool for ensuring SOC2 compliance.
You write professional, serious, and persuasive cold emails.
"""

ENGAGING_INSTRUCTIONS = """
You are a sales agent working for ComplAI, a company that provides a SaaS tool for ensuring SOC2 compliance.
You write witty, engaging, and creative cold emails that are likely to get a response.
"""

BUSY_INSTRUCTIONS = """
You are a sales agent working for ComplAI, a company that provides a SaaS tool for ensuring SOC2 compliance.
You write concise, to-the-point, and impactful cold emails that respect the reader's time.
"""

EMAILER_INSTRUCTIONS = """
You are an email formatter and sender. Your process is strict and sequential:
1. First, you MUST use the `subject_writer` tool to write a subject for the email body you receive.
2. Then, you MUST use the `html_converter` tool to convert the text body to HTML.
3. Finally, you MUST use the `send_html_email` tool to send the email with the generated subject and HTML body.
"""

SALES_MANAGER_INSTRUCTIONS = """
You are a sales manager at ComplAI. Your goal is to create and send the most effective cold sales email.
Your workflow is as follows:
1. You MUST use all three writer tools (professional_writer, engaging_writer, busy_writer) to generate three different versions of the email based on the user's request.
2. You MUST analyze the three versions and select the single best one based on your expert judgment of which email will be most effective.
3. Once you have chosen the best email body, you MUST handoff to the Email_Manager agent to handle the final formatting and sending.
"""


# --- 4. Tool Definitions (Python Functions) ---

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Sends an email with the given subject and HTML body using the SendGrid API.

    Note: This function is currently mocked to print to the console instead of
    sending a real email. To enable, uncomment the SendGrid code and provide
    a valid API key and verified sender email.

    Args:
        subject (str): The subject line of the email.
        html_body (str): The body of the email in HTML format.

    Returns:
        Dict[str, str]: A dictionary confirming the success of the operation.
    """
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("YOUR_VERIFIED_SENDER@example.com")  # IMPORTANT: Change to your verified sender
    to_email = To("RECIPIENT@example.com")                  # IMPORTANT: Change to your recipient
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send(mail)
    
    print("--- 📧 Mock Email Sent Successfully 📧 ---")
    print(f"Subject: {subject}")
    print(f"HTML Body:\n{html_body}")
    print("---------------------------------------")
    return {"status": "success"}


# --- 5. Agent Definitions ---

def initialize_agent_system() -> Agent:
    """
    Initializes and assembles the complete hierarchical multi-agent system.

    This function defines all specialist agents, converts them into tools where
    necessary, and constructs the manager agents that orchestrate the workflow.

    Returns:
        Agent: The top-level Sales_Manager agent, ready for execution.
    """
    
    # --- Level 1: Specialist "Worker" Agents ---
    # These agents perform a single, well-defined task.

    professional_writer = Agent(name="Professional_Writer", instructions=PROFESSIONAL_INSTRUCTIONS, model="gpt-4o-mini")
    engaging_writer = Agent(name="Engaging_Writer", instructions=ENGAGING_INSTRUCTIONS, model="gpt-4o-mini")
    busy_writer = Agent(name="Busy_Writer", instructions=BUSY_INSTRUCTIONS, model="gpt-4o-mini")
    
    subject_writer = Agent(name="Subject_Writer", instructions="You write compelling subjects for cold sales emails.", model="gpt-4o-mini")
    html_converter = Agent(name="HTML_Converter", instructions="You convert a markdown email body to a simple HTML body.", model="gpt-4o-mini")

    # --- Level 2: Convert Agents into Tools ---
    # These agents are packaged as tools to be used by manager agents.
    
    professional_tool = professional_writer.as_tool(tool_name="professional_writer", tool_description="Writes a sales email in a professional and serious tone.")
    engaging_tool = engaging_writer.as_tool(tool_name="engaging_writer", tool_description="Writes a sales email in a witty and engaging tone.")
    busy_tool = busy_writer.as_tool(tool_name="busy_writer", tool_description="Writes a sales email in a concise and to-the-point tone.")
    
    subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Writes a subject line for an email body.")
    html_tool = html_converter.as_tool(tool_name="html_converter", tool_description="Converts an email body from text/markdown to HTML.")
    
    # --- Level 3: Sub-System "Manager" Agent ---
    # This agent manages a specific sub-workflow (formatting and sending).
    
    emailer_agent = Agent(
        name="Email_Manager",
        instructions=EMAILER_INSTRUCTIONS,
        tools=[subject_tool, html_tool, send_html_email],
        model="gpt-4o-mini",
        handoff_description="This agent handles the final steps: creating a subject, converting the body to HTML, and sending the email."
    )
    
    # --- Level 4: Top-Level "Orchestrator" Agent ---
    # This agent manages the entire process from start to finish.
    
    sales_manager = Agent(
        name="Sales_Manager",
        instructions=SALES_MANAGER_INSTRUCTIONS,
        tools=[professional_tool, engaging_tool, busy_tool],
        handoffs=[emailer_agent],  # Defines the agent to handoff to after its primary tasks are complete.
        model="gpt-4o-mini"
    )
    
    return sales_manager


# --- 6. Main Execution Block ---

async def main():
    """
    The main entry point for running the automated sales email pipeline.
    """
    # Initialize the entire agent system.
    sales_manager_agent = initialize_agent_system()
    
    # Define the initial user prompt that kicks off the workflow.
    initial_message = "Send a cold sales email to the CEO of a fast-growing tech startup, introducing our AI-powered SOC2 compliance tool, 'ComplAI'. Please sign the email from 'Alice'."

    print("🚀 Starting Automated Sales SDR Workflow...")
    
    # Use the 'track' context manager to log all agent interactions for debugging.
    with track("Automated_SDR_Workflow_Run"):
        # The 'run' function executes the top-level agent with the initial message.
        result = await run(sales_manager_agent, initial_message)
        
    print("\n🏁 Workflow Finished. Final Result:")
    pprint(result)

if __name__ == "__main__":
    # Run the main asynchronous function.
    asyncio.run(main())