# -*- coding: utf-8 -*-
"""
04_D04_DeepSearch.py

This script demonstrates an AI-driven multi-agent system for planning web searches,
performing them asynchronously, synthesizing a detailed report, and sending the report via email.

Original notebook location:
https://colab.research.google.com/drive/1mO0oyRgavafWtLjNHXRvRjdRSdE54FSt
"""

import asyncio
import os
from typing import Dict, List

from agents import (
    Agent,
    WebSearchTool,
    trace,
    Runner,
    function_tool,
)
from agents.model_settings import ModelSettings
from pydantic import BaseModel
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from IPython.display import display, Markdown

# Load environment variables from .env file (overriding existing ones)
load_dotenv(override=True)

# ------------------------
# Define the Search Agent
# ------------------------

SEARCH_AGENT_INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points succinctly without extra commentary or perfect grammar. "
    "This will be used by someone synthesizing a report, so focus on essence and ignore fluff."
)

search_agent = Agent(
    name="Search Agent",
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

# -----------------------------------
# Define Planner Agent and Data Models
# -----------------------------------

HOW_MANY_SEARCHES = 3

PLANNER_AGENT_INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."
)

class WebSearchItem(BaseModel):
    reason: str
    """Reason why this search term is important to answer the query."""

    query: str
    """The search term to use for the web search."""

class WebSearchPlan(BaseModel):
    searches: List[WebSearchItem]
    """List of web searches to perform to best answer the query."""

planner_agent = Agent(
    name="Planner Agent",
    instructions=PLANNER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)

# -------------------
# Email Sending Tool
# -------------------

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an email with the specified subject and HTML content.
    
    Args:
        subject (str): Email subject line.
        html_body (str): Email content in HTML format.
        
    Returns:
        Dict[str, str]: Status dictionary indicating success.
    """
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("YOUR_EMAIL_ADDRESS")  # Replace with your verified sender email
    to_email = To("YOUR_EMAIL_ADDRESS")       # Replace with recipient email
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

# -----------------------
# Define Email Agent
# -----------------------

EMAIL_AGENT_INSTRUCTIONS = (
    "You are able to send a nicely formatted HTML email based on a detailed report. "
    "You will be provided with a detailed report. Use your tool to send one email, "
    "converting the report into clean, well-presented HTML with an appropriate subject."
)

email_agent = Agent(
    name="Email Agent",
    instructions=EMAIL_AGENT_INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)

# -----------------------
# Define Writer Agent
# -----------------------

WRITER_AGENT_INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided the original query and some initial research done by an assistant.\n"
    "First, create an outline describing the structure and flow of the report. "
    "Then generate the full report and return it as your final output in markdown format.\n"
    "The report should be detailed, 5-10 pages, at least 1000 words."
)

class ReportData(BaseModel):
    short_summary: str
    """A brief 2-3 sentence summary of findings."""

    markdown_report: str
    """The detailed final report in markdown format."""

    follow_up_questions: List[str]
    """List of suggested topics for further research."""

writer_agent = Agent(
    name="Writer Agent",
    instructions=WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)

# -----------------------------------
# Async Functions to Plan and Execute Search
# -----------------------------------

async def plan_searches(query: str) -> WebSearchPlan:
    """
    Use the planner agent to generate a plan of web searches for the given query.

    Args:
        query (str): The research query to plan searches for.

    Returns:
        WebSearchPlan: A structured plan containing a list of search items.
    """
    print("Planning searches...")
    result = await Runner.run(planner_agent, f"Query: {query}")
    print(f"Will perform {len(result.final_output.searches)} searches")
    return result.final_output

async def search(item: WebSearchItem) -> str:
    """
    Execute a single web search using the search agent.

    Args:
        item (WebSearchItem): A search item containing the query and reason.

    Returns:
        str: The concise summary of the search results.
    """
    input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
    result = await Runner.run(search_agent, input_text)
    return result.final_output

async def perform_searches(search_plan: WebSearchPlan) -> List[str]:
    """
    Perform all planned web searches concurrently.

    Args:
        search_plan (WebSearchPlan): The search plan containing all search items.

    Returns:
        List[str]: List of search results summaries.
    """
    print("Performing searches...")
    tasks = [asyncio.create_task(search(item)) for item in search_plan.searches]
    results = await asyncio.gather(*tasks)
    print("Finished all searches.")
    return results

# -----------------------------------
# Async Functions to Write Report and Send Email
# -----------------------------------

async def write_report(query: str, search_results: List[str]) -> ReportData:
    """
    Use the writer agent to compose a detailed research report.

    Args:
        query (str): The original research query.
        search_results (List[str]): Summarized results from web searches.

    Returns:
        ReportData: Structured report data including markdown report and summary.
    """
    print("Writing report...")
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_text)
    print("Report writing complete.")
    return result.final_output

async def send_report_email(report: ReportData) -> ReportData:
    """
    Use the email agent to send the report via email.

    Args:
        report (ReportData): The report data to send.

    Returns:
        ReportData: The same report data (for chaining).
    """
    print("Sending email...")
    await Runner.run(email_agent, report.markdown_report)
    print("Email sent successfully.")
    return report

# -----------------------
# Main Execution Workflow
# -----------------------

async def main():
    query = "Latest AI Agent frameworks in 2025"
    with trace("Research trace"):
        print("Starting research workflow...")
        search_plan = await plan_searches(query)
        search_results = await perform_searches(search_plan)
        report = await write_report(query, search_results)
        await send_report_email(report)
        print("Research workflow completed successfully!")

# If running interactively or script entry point, you can start the main event loop like this:
# asyncio.run(main())

