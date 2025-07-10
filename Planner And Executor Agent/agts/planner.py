# planner.py
from openai import OpenAI # Import the client type hint
from models.schema import Task
from typing import List
import json

# The function now requires the client to be passed in
def call_llm(client: OpenAI, prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# This function also needs the client
def plan_tasks(client: OpenAI, goal: str) -> List[Task]:
    system_prompt = f"""You are a planning agent. Your goal is to break down this task into 5 to 8 numbered steps.
                        Each step should have a clear title and description.
                        Task: {goal}
                        
                        You must respond in a valid JSON format. The JSON should be an object with a single key "tripPlanningSteps" 
                        that contains a list of objects, where each object has the following keys: "step", "title", "description"."""
    
    content = call_llm(client, system_prompt)
    
    print(f"DEBUG: Raw content from LLM before parsing:\n---\n{content}\n---")
    
    parsed = json.loads(content)
    
    return [Task(**item) for item in parsed['tripPlanningSteps']]