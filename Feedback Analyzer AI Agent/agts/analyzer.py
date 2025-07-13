# feedback analyzer agent
from openai import OpenAI
from pathlib import Path
from utils import load_prompt
from .schemas import AnalysisResult

class FeedbackAnalyzerAgent:
    def __init__(self, client: OpenAI, prompt_path: Path):
        self.client = client
        self.prompt_path = prompt_path

    def run(self, text) -> AnalysisResult:
        # Load Prompt
        prompt_content = load_prompt(self.prompt_path, {"TEXT": text})

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_content}],
            temperature=0.5,
            response_format={'type': 'json_object'},)
        # Get response
        content = response.choices[0].message.content.strip()

        # Validate and parse the JSON response
        try:
            parsed_sentiment = AnalysisResult.model_validate_json(content)
            return parsed_sentiment
        except Exception as e:
            print(f"[FeedbackAnalyzerAgent] Error Parsing Json: {e}")
            print(f"[FeedbackAnalyzerAgent] Raw Response from Model: \n{content}")
            raise ValueError("Failed to Parse Sentiment from Model Response.")