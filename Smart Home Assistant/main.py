import asyncio
from smart_agent import create_smart_home_agent
from agents import Runner, trace
from dotenv import load_dotenv

load_dotenv()

async def main():
    """Main function to run the Smart Home Assistant"""
    # create the agent instance
    home_agent = create_smart_home_agent()
    # Define complex command
    command = """Set the thermostat to 22°C in the living room
                 and turn on the light in the kitchen at 50% brightness.
                 can you also play some music by Vivaldi, maybe 'The Four Seasons'"""
    
    with trace("Smart Home Assistant"):
        result = await Runner.run(home_agent, command)
    print(f"Final Response to User:\n{result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())