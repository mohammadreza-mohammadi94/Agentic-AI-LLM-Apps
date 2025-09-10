# /tools/definitions.py

def get_tool_definitions(use_cases: list[str] | None = None) -> list[dict]:
    """
    Returns the JSON schema definitions for tools. Can be filtered by use case.
    
    Args:
        use_cases (list[str] | None): A list of tool names to include. 
                                      If None, all tools are returned.
    """
    all_tools = {
        "prioritize_tasks": {
            "type": "function",
            "function": {
                "name": "prioritize_tasks",
                "description": "Analyzes a list of tasks and returns them in a prioritized order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tasks": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "The full list of task objects to be prioritized."
                        }
                    },
                    "required": ["tasks"]
                }
            }
        },
        "schedule_task": {
            "type": "function",
            "function": {
                "name": "schedule_task",
                "description": "Schedules a single task on the user's calendar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_name": {
                            "type": "string",
                            "description": "The name of the task to schedule."
                        },
                        "start_time": {
                            "type": "string",
                            "description": "The start time for the event in HH:MM format (e.g., '14:30')."
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time for the event in HH:MM format (e.g., '15:30')."
                        }
                    },
                    "required": ["task_name", "start_time", "end_time"]
                }
            }
        }
    }
    
    if use_cases:
        return [tool for name, tool in all_tools.items() if name in use_cases]
        
    return list(all_tools.values())