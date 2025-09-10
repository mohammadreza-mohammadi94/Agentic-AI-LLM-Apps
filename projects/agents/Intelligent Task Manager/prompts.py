# /prompts.py

def get_prioritization_prompt() -> str:
    """The prompt used by the prioritization step."""
    return """
You are a prioritization engine. Your sole purpose is to analyze the following list of tasks and return a JSON object containing a single key, "prioritized_order", with a list of the task names sorted by urgency and importance. The most critical task should be first. Do not provide any other explanation or text.

Tasks:
{tasks_json}
"""

def get_scheduling_prompt(task_name: str) -> str:
    """The prompt for scheduling a single task."""
    return f"""
You are an intelligent task scheduler. Your goal is to schedule the following single task: '{task_name}'.

You MUST call the `schedule_task` tool to place this task on the calendar. Make a logical assumption about the task's duration to determine the start and end times.
"""