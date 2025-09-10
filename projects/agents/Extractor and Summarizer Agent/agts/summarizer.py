# agents/summarizer.py
from openai import OpenAI
from pathlib import Path
from utils import load_prompt

class SummarizerAgent:
    """
    An agent that summarizes a given text using an OpenAI model.
    """
    def __init__(self, client: OpenAI, prompt_path: Path):
        """
        Initializes the SummarizerAgent.

        Args:
            client (OpenAI): An instance of the OpenAI client.
            prompt_path (Path): The file path to the prompt template.
        """
        self.client = client
        self.prompt_path = prompt_path

    def run(self, text: str) -> str:
        """
        Generates a summary for the given text.

        [cite_start]The prompt instructs the model to generate a summary in Farsi[cite: 2].

        Args:
            text (str): The input text to summarize.

        Returns:
            str: The generated summary as a string.
        """
        # Load the prompt template and inject the text.
        prompt = load_prompt(self.prompt_path, text)

        # Call the OpenAI API.
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # A bit of creativity for fluent summarization
        )

        # Return the summary content.
        return response.choices[0].message.content.strip()