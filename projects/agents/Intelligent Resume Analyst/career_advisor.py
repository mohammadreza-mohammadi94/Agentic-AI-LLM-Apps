# /career_advisor.py
"""This is the core orchestrator, containing the main business logic."""

from llm_clients import query_advisor, query_evaluator
from prompts import get_advisor_prompt, get_evaluator_prompt
from config import MAX_RETRIES

class CareerAdvisor:
    """
    Handles the logic of getting and evaluating career advice.
    """
    def get_advice(self, resume_text: str, question: str) -> str:
        """
        Gets career advice, evaluates it, and retries if necessary.
        """
        feedback = ""
        for attempt in range(MAX_RETRIES):
            print(f"--- Attempt {attempt + 1} ---")

            # 1. Get advice
            advisor_prompt = get_advisor_prompt(resume_text, question, feedback)
            advice = query_advisor(advisor_prompt)
            print(f"Advisor says: {advice[:100]}...")

            # 2. Evaluate the advice
            evaluator_prompt = get_evaluator_prompt(resume_text, question, advice)
            evaluation = query_evaluator(evaluator_prompt)
            print(f"Evaluator says: {evaluation}")

            # 3. Check evaluation and decide next step
            if evaluation.startswith("ACCEPT"):
                return advice
            else:
                feedback = evaluation.replace("REJECT:", "").strip()

        return "I apologize, but I'm having trouble providing a high-quality response right now. Please try rephrasing your question."