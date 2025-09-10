from agents import Agent
from app_agents.models import SearchDecision

INSTRUCTION = """
You are a decision agent. Given a user's question, decide if the answer requires web search.
Only respond with 'YES' if search is needed, otherwise 'NO'.
No extra text, no explaination
"""

decision_agent = Agent(
    name="DecisionAgent",
    instructions=INSTRUCTION,
    model="gpt-4o-mini",
    output_type=SearchDecision
)