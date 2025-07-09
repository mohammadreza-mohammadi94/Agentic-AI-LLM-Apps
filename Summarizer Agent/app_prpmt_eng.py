"""
Counts the number of words in a given text by leveraging prompt engineering with a language model.

This function sends a prompt to a language model asking it to count the words in the input text
and returns the count as interpreted by the model.

No external tokenization libraries like NLTK are used; instead, the model processes the text directly
based on the prompt instructions.
"""
#-----------------------#
# Load Libraries        #
#-----------------------#
from agents import Agent, Runner, trace
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel, Field

# Load env
load_dotenv(override=True)

# Define basemodel for summary
class SummaryOutput(BaseModel):
    summary: str = Field(..., description="Concise summary with max 300 words.")


#-----------------------#
# Define Agents         #
#-----------------------#

# Summarizer Agent
# Define instruction for summarizer
SUMMARIZER_INSTRUCTION = (
    "You are a summarizer agent. Your task is to produce a concise and accurate summary of the input text. "
    "The summary must not exceed 300 words. "
    "Avoid repetition and keep it clear and focused."
)

# Define Summarizer Agent
summarizer_agent = Agent(
    name="SummarizerAgent",
    instructions=SUMMARIZER_INSTRUCTION,
    model="gpt-4o-mini",
    output_type=SummaryOutput
)

# WordCount Agent
# Define instrunction for WordCountAgent
WORDCOUNT_INSTRUCTION = (
        "You receive a text input. Your task is to count and return only the number of words in the input text. "
        "Respond with the number only, no explanations."
    )

# Define WordCount Agent
word_count_agent = Agent(
    name="WordCountAgent",
    instructions=WORDCOUNT_INSTRUCTION,
    model="gpt-4o-mini"
)

#-----------------------#
# Define Functions      #
#-----------------------#

async def count_words(text: str) -> int:
    """Count number of words in text by prompting the LLM Agent,
    to count words
    """
    with trace("WordCount"):
        result = await Runner.run(word_count_agent, text)
        output = result.final_output.strip()

    # Parse the number from the output
    try:
        count = int(''.join(filter(str.isdigit, output)))
        return count
    except Exception:
        print(f"Warning: could not parse word count from output: {output}")
        return -1
    


async def main():
    # Run word count agent
    file_path = '<YOUR_FILE_PATH>'
    with open(file_path, 'r', encoding='utf-8') as f:
        my_text = f.read()

    original_word_count = await count_words(my_text)
    print(f"Original Text Length: {original_word_count} words")

    # Run Summarizer Agent
    with trace("Summarizer"):
        result = await Runner.run(summarizer_agent, my_text)
        summary_text = result.final_output.summary

    summary_word_count = await count_words(summary_text)
    print(f"Summary Length: {summary_word_count} words")
    print("\nSummary:\n", summary_text)

    if summary_word_count > 300:
        print("\nWarning: Summary exceeds 300 words. Consider revising instructions or truncating summary.")


if __name__ == '__main__':
    asyncio.run(main())