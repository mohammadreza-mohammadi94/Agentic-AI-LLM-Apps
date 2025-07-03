# /tools/implementations.py
import json
import openai
from config import OPENAI_API_KEY, MODEL_NAME
from prompts import get_prioritization_prompt

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# --- Tool Implementations ---

def prioritize_tasks(tasks: list[dict]) -> str:
    """A 'smart' tool that uses an LLM to prioritize tasks."""
    print("🛠️  Tool: Running task prioritization...")
    
    prompt = get_prioritization_prompt().format(tasks_json=json.dumps(tasks, indent=2))
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        # The response from this LLM call is the data we need
        prioritized_data = response.choices[0].message.content
        return json.dumps(json.loads(prioritized_data))
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error prioritizing tasks: {e}"

def schedule_task(task_name: str, start_time: str, end_time: str) -> str:
    """
    A mock function to simulate adding a task to a calendar API.
    """
    print(f"🗓️  Tool: Scheduling '{task_name}' from {start_time} to {end_time}.")
    # In a real application, this would make an API call to Google Calendar, etc.
    return f"Success: '{task_name}' has been scheduled on the calendar from {start_time} to {end_time}."

# --- Tool Dispatcher ---
AVAILABLE_TOOLS = {
    "prioritize_tasks": prioritize_tasks,
    "schedule_task": schedule_task,
}