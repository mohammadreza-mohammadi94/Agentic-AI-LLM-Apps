"""
This module centralizes all configurations.
"""
# /config.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- API Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY") # <-- ADD THIS

if not OPENAI_API_KEY or not NEWS_API_KEY:
    raise ValueError("API keys for OpenAI and NewsAPI must be set in the .env file.")

# --- Model Configuration ---
ANALYSIS_MODEL = "gpt-4o-mini"

# --- Project Configuration ---
# The financial topic or company to research (e.g., stock ticker)
FINANCIAL_TOPIC = "NVIDIA"

# Directory to save the output reports
OUTPUT_DIR = "/output"