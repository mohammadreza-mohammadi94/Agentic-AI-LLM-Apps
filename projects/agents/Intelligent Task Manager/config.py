# /config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file.")


MODEL_NAME = "gpt-4o-mini"
TASKS_FILE_PATH = "sample_task.json"