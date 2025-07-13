# agents/extractor.py
from openai import OpenAI
from pathlib import Path
from utils import load_prompt
from .schemas import ExtractedEntities

class ExtractorAgent:
    """
    An agent that extracts named entities from a given text using an OpenAI model.
    """
    def __init__(self, client: OpenAI, prompt_path: Path):
        """
        Initializes the ExtractorAgent.

        Args:
            client (OpenAI): An instance of the OpenAI client.
            prompt_path (Path): The file path to the prompt template.
        """
        self.client = client
        self.prompt_path = prompt_path

    def run(self, text: str) -> ExtractedEntities:
        """
        Extracts entities from the text based on the provided prompt.

        Args:
            text (str): The input text to process.

        Returns:
            ExtractedEntities: A Pydantic model containing the extracted entities.
        
        Raises:
            ValueError: If the model's response cannot be parsed into JSON.
        """
        # Load the prompt template and inject the text.
        prompt_content = load_prompt(self.prompt_path, text)

        # Call the OpenAI API.
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_content}],
            temperature=0.0,  # Low temperature for deterministic output
            response_format={"type": "json_object"} # Use JSON mode for reliable output
        )

        # Get the response content.
        content = response.choices[0].message.content.strip()

        # Validate and parse the JSON response using the Pydantic model.
        try:
            parsed_entities = ExtractedEntities.model_validate_json(content)
            return parsed_entities
        except Exception as e:
            print(f"[ExtractorAgent] Error parsing JSON: {e}")
            print(f"[ExtractorAgent] Raw response from model:\n{content}")
            raise ValueError("Failed to parse entities from model response.") from e