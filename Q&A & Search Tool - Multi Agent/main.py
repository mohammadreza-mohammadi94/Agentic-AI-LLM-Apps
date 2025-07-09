#-----------------------#
# Load Libraries        #
#-----------------------#
# main.py
import asyncio
from dotenv import load_dotenv
import os

from agents import Runner, trace
from app_agents.decision_agent import decision_agent
from app_agents.search_agents import search_agent
from app_agents.models import SearchDecision


# Load env
load_dotenv(override=True)

async def main():
    query = "What are the top AI conferences in 2025?"

    # DecisionAgent
    with trace("DecisionAgent"):
        descision_result = await Runner.run(decision_agent, query)
        decision = descision_result.final_output.decision
        print(f"Decision Agent Output: {decision}")
    
    if decision == "YES":
        with trace("SearchAgent"):
            search_result = await Runner.run(search_agent, query)
            print("Search Agent Output:\n", search_result.final_output)
    else:
        print("No search needed; answer can be provided directly.")

if __name__ == "__main__":
    asyncio.run(main())
