from agents import Agent
from prompts import SMART_HOME_SYSTEM_PROMPT
import tools as T

def create_smart_home_agent():
    """Factory function to create a Smart Home Assistant Agent"""
    tool_list = [
        T.set_thermostat,
        T.turn_light_on,
        T.play_music
    ]

    smart_home_agent = Agent(
        name="Smart Home Assistant",
        instructions=SMART_HOME_SYSTEM_PROMPT,
        model="gpt-4o-mini",
        tools=tool_list
    )

    return smart_home_agent