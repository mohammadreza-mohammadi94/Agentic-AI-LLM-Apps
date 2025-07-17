import os
import asyncio
from typing import Dict, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pprint import pprint
import markdown2
from agents import (Agent, 
                    Runner, 
                    trace, 
                    function_tool, 
                    OpenAIChatCompletionsModel)

# Configuration
print("Loading enviorment variables...")
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found system enviorment.")

# Define schema
class ResearchPlan(BaseModel):
    steps: List[str] = Field(description="A list of clear, actionable steps to conduct the market research.")


# Define tools
@function_tool
def web_search_tool(query: str) -> str:
    """
    Simulates a web search for a given query.
    In a real application, this would use a real search API (e.g., Tavily, Google Search).
    """
    print(f"--- TOOL: Search web for {query} ---")
    mock_result = {
        "LLM providers in 2025": "Key LLM providers in 2025 include OpenAI (GPT series), Google (Gemini series), Anthropic (Claude series), and various open-source models like Llama 3 running on platforms like Groq for high-speed inference.",
        "Market share analysis of LLMs": "Market analysis indicates a competitive landscape where OpenAI holds a significant share, but competitors like Anthropic and Google are rapidly gaining ground. Open-source models are also becoming increasingly popular in enterprise applications.",
        "Future trends in LLM market": "Future trends point towards smaller, more efficient specialized models, multi-modal capabilities, and a greater emphasis on on-premise and private cloud deployments for data security."
    }
    return mock_result.get(query, "No information found for this query.")

@function_tool
def send_email_tool(recipient: str, subject: str, html_body: str) -> Dict[str, str]:
    """
    Simulates sending an email with a given subject and HTML body.
    In a real application, this would use an email service like SendGrid.
    """
    print("--- 📧 TOOL: Sending final email report ---")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body (HTML):\n{html_body}")
    print("------------------------------------------")
    return {"status": "success", "message": f"Email successfully sent to {recipient}."}

@function_tool
def markdown_to_html_tool(markdown_text: str) -> str:
    """Converts a string of Markdown text to HTML."""
    print("--- 🛠️ TOOL: Converting report from Markdown to HTML ---")
    return markdown2.markdown(markdown_text)

# Agent Definition
def initialize_agents() -> Dict[str, Agent]:
    """
    Initializes and returns a dictionary of all specialized agents in the system.
    """
    print("Initializing specialized agents...")

    planner_instructions = """
    You are an expert research planner. Your goal is to create a clear, step-by-step plan based on a user's high-level request.
    You MUST produce a structured output that conforms to the `ResearchPlan` schema, which includes a list of actionable steps.
    For example, if the request is to analyze LLM providers, your output should be a list of steps like:
    - "Identify major LLM providers in 2025."
    - "Analyze market share of LLM providers."
    - "Research future trends in the LLM market."
    Ensure the steps are clear, specific, and actionable.
    """

    # Agent 1: The Planner
    planner_agent = Agent(
        name="Planner_Agent",
        instructions=planner_instructions,
        output_type=ResearchPlan,
        model="gpt-4o-mini"
    )

    # Agent 2: The Searcher
    search_agent = Agent(
        name="Search_Agent",
        instructions="You are an expert web researcher. You use the web_search_tool to find information based on a given query.",
        tools=[web_search_tool],
        model="gpt-4o-mini"
    )

    # Agent 3: The Report Writer
    writer_agent = Agent(
        name="Report_Writer_Agent",
        instructions="You are an expert technical writer. You synthesize research findings into a well-structured and insightful report in Markdown format.",
        model="gpt-4o-mini"
    )

    # Agent 4: The Emailer
    emailer_agent = Agent(
        name="Emailer_Agent",
        instructions="You are an email specialist. First, convert the provided Markdown report to HTML using the markdown_to_html_tool. Then, send the resulting HTML report using the send_email_tool. The subject should be a summary of the report.",
        tools=[markdown_to_html_tool, send_email_tool],
        model="gpt-4o-mini"
    )
    
    return {
        "planner": planner_agent,
        "searcher": search_agent,
        "writer": writer_agent,
        "emailer": emailer_agent,
    }

#Main Orchestration Logic
async def main():
    """
    The main orchestrator function that runs the entire agentic workflow.
    """
    # The high-level goal provided by the user
    initial_goal = "Create a market analysis report of LLM providers in 2025."
    recipient_email = "team_lead@example.com"
    
    print(f"🚀 Starting automated workflow for goal: '{initial_goal}'")
        
    with trace("Auto_Seach_And_Report"):
        agents = initialize_agents()
        print(f"--- Phase 1: Planning ---")
        plan_result = await Runner.run(agents["planner"], f"Create a research plan for the goal: {initial_goal}")

        if not isinstance(plan_result, ResearchPlan) or not plan_result.steps:
            print("Warning: Planner Agent did not return a valid plan. Using fallback plan.")
            plan_result = ResearchPlan(steps=[
                "Identify major LLM providers in 2025.",
                "Analyze market share of LLM providers.",
                "Research future trends in the LLM market."
            ])
        
        research_plan = plan_result.steps
        print(f"Plan clreated successfully: {research_plan}")

        # Step 2
        print("\n--- Phase 2: Searching ---")
        research_findings = []
        for step in research_plan:
            # For each step in the plan, use the search agent to find information
            finding = await Runner.run(agents["searcher"], step)
            research_findings.append(finding)
        
        print(f"✅ Research complete. {len(research_findings)} pieces of information gathered.")
        
        # Step 3
        print("\n--- Phase 3: Writing Report ---")
        # Combine all findings into a single context for the writer agent
        full_context = "\n\n".join(research_findings)
        report_markdown = await Runner.run(agents["writer"], f"Write a comprehensive report based on the following research findings:\n\n{full_context}")
        
        print("✅ Report written successfully in Markdown.")
        # print(f"\n--- Generated Report (Markdown) ---\n{report_markdown}\n--------------------")

        # Step 4
        print("\n--- Phase 4: Formatting and Sending Email ---")
        # The emailer agent takes the report and handles the rest
        email_prompt = f"""
        Please send the following market research report to '{recipient_email}'.
        The subject of the email should be 'Market Analysis Report: LLM Providers in 2025'.
        
        Report Content:
        {report_markdown}
        """
        final_result = await Runner.run(agents["emailer"], email_prompt)
        
        print("\n🏁 Workflow Finished.")
        pprint(final_result)


if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())