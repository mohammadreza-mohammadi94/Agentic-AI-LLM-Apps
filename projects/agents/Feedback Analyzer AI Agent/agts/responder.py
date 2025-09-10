from openai import OpenAI
from pathlib import Path
from utils import load_prompt

class ResponseGeneratorAgent:
    def __init__(self, client: OpenAI, prompt_path: Path):
        self.client = client
        self.prompt_path = prompt_path

    def run(self, problem_summary) -> str:
        # Load Prompt
        prompt = load_prompt(self.prompt_path, 
                             {"PROBLEM_SUMMARY": problem_summary})
        # Call OPENAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        # Return Reponse
        return response.choices[0].message.content.strip()
    
