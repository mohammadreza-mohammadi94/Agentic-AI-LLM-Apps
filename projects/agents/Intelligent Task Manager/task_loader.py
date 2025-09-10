# /task_loader.py

import json

def load_tasks_from_json(filepath):
    """Loads a list of tasks from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading tasks from {filepath}: {e}")
        return None
