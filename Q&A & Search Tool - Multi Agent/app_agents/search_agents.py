from agents import Agent, WebSearchTool

INSTRUCTION = """
You are a helpful assistant that performs web search to answer user queries.add()
Search the web using available tools and produce a concise summary of the results.
"""

search_agent = Agent(
    name="SearchAgent",
    instructions=INSTRUCTION,
    model="gpt-4o-mini",
    tools=[WebSearchTool()]
)
