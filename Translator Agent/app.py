#-----------------------#
# Load Libraries        #
#-----------------------#
from agents import Agent, Runner, trace
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import asyncio


#-----------------------#
# Agent Configuration   #
#-----------------------#
# Load env
load_dotenv(override=True)

# Define BaseModel for Translation
class TranslationOutput(BaseModel):
    translate: str = Field(..., description="Translate from English to Farsi.")

#-----------------------#
# Define Agents         #
#-----------------------#
# Translator Agent
# Define instruction for translation
TRANSLATOR_INSTRUCTION = (
    "You are a translator agent.\n" 
    "Your task is to produce concise and accurate translation from 'English' to 'Farsi'"
    "Avoid add additional text to translation.\n"
    "ONLY provide Accurate translation from English to Persian without adding text to the translation text"
)

# Define TranslateAgent
translator_agent = Agent(
    name="TranslatorAgent",
    instructions=TRANSLATOR_INSTRUCTION,
    model="gpt-4o-mini",
    output_type=TranslationOutput
)

async def main():
    """Main async entry point to run TranslatorAgent on sample query."""
    query = "I'm a Dedicated Data Scientist and Machine Learning Engineer with over 6 years of programming experience, including 5 years specializing in machine learning and deep learning."
    with trace("Translate"):
        result = await Runner.run(translator_agent, query)
        translation = result.final_output.translate
        print(translation.strip())

if __name__ == '__main__':
    asyncio.run(main())