# /debate_simulator.py

"""
This is the beating heart of the project. 
The main logic of the orchestration of the debate 
and evaluation is located in this module.
"""
import json

from llm_clients import query_llm
from prompts import get_debate_prompt, get_judge_prompt

class DebateSimulator:
    """
    Orchestrates a debate between multiple LLMs and evaluates the outcome.
    """
    def __init__(self, debaters, judge):
        """
        Initializes the simulator with debaters and a judge.

        Args:
            debaters (List[Dict[str, str]]): A list of dictionaries, each
                representing a debater with 'provider', 'model', and 'stance'.
            judge (Dict[str, str]): A dictionary representing the judge LLM.
        """
        self.debaters_config = debaters
        self.judge_config = judge
        self.arguments = {}

    def run_debate(self):
        """
        Collects arguments from all configured debater LLMs.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the arguments,
            where keys are debater names (e.g., 'Debater_Pro').
        """
        print("---- Starting the Debater ----")
        for i, debater in enumerate(self.debaters_config):
            stance = debater['stance']
            model = debater['model']
            provider = debater['provider']
            debater_name = f"Debater_{stance.capitalize()}"

            print(f"🗣️  Querying {debater_name} (Model: {model}) for a '{stance}' argument...")

            prompt = get_debate_prompt(stance)
            argument = query_llm(provider, model, prompt)

            self.arguments[debater_name] = {
                "stance": stance,
                "model": model,
                "argument": argument
            }
        print(f"---- All arguments collected ----\n")
        return self.arguments
    
    def evaluate_debate(self):
        """
        Uses a judge LLM to evaluate and rank the collected arguments.

        Returns:
            Dict[str, Any]: A dictionary containing the ranked list of arguments
            and the judge's reasoning, parsed from the judge's JSON output.
        """
        if not self.arguments:
            raise ValueError("Debate has not been run yet. Call run_debate() first.")
        print("--- Starting Evaluation ---")
        print(f"⚖️  Sending arguments to the Judge (Model: {self.judge_config['model']})...")
        
        judge_prompt = get_judge_prompt(self.arguments)
        
        # Query the judge model, ensuring we request JSON output
        judge_response_str = query_llm(
            provider=self.judge_config['provider'],
            model=self.judge_config['model'],
            prompt=judge_prompt,
            is_json=True
        )
        
        print("---- Evaluation received ----\n")

        try:
            # Parse the JSON response from the judge
            ranked_results = json.loads(judge_response_str)
            return ranked_results
        except json.JSONDecodeError:
            print("Error: Judge did not return valid JSON. Here is the raw response:")
            print(judge_response_str)
            # Return a structured error message
            return {"error": "Failed to parse JSON from judge.", "raw_response": judge_response_str}
