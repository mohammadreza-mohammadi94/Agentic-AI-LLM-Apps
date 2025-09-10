# main.py
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from agts.summarizer import SummarizerAgent
from agts.extractor import ExtractorAgent
from agts.schemas import ExtractedEntities
from sample_input import TEXT_INPUT

# --- Configuration ---
load_dotenv()  # Load variables from .env file

# Define key directories and file paths
PROMPTS_DIR = Path("prompts")
OUTPUT_DIR = Path("output")
EXTRACTOR_PROMPT_PATH = PROMPTS_DIR / "extractor_prompt.txt"
SUMMARIZER_PROMPT_PATH = PROMPTS_DIR / "summarizer_prompt.txt"
# Define output file paths
ENTITIES_OUTPUT_PATH = OUTPUT_DIR / "entities.json"
SUMMARY_OUTPUT_PATH = OUTPUT_DIR / "summary.txt"
MARKDOWN_REPORT_PATH = OUTPUT_DIR / "report.md"


def create_markdown_report(summary: str, entities: ExtractedEntities) -> str:
    """
    Generates a markdown report from the summary and extracted entities.

    Args:
        summary (str): The summary text.
        entities (ExtractedEntities): The Pydantic model of extracted entities.

    Returns:
        str: A string containing the full report in Markdown format.
    """
    report_parts = []
    # --- Summary Section ---
    report_parts.append("## 📝 خلاصه")
    report_parts.append(summary)
    report_parts.append("\n---\n") # Thematic break

    # --- Entities Section ---
    report_parts.append("## 🔍 موجودیت‌های استخراج‌شده")
    # Table header
    report_parts.append("| دسته (Category) | موارد یافت‌شده (Entities) |")
    report_parts.append("|:---|:---|")

    # Table rows
    entity_dict = entities.model_dump()
    for category, items in entity_dict.items():
        # Join list items into a comma-separated string, or show "N/A" if empty
        display_items = ", ".join(f"`{item}`" for item in items) if items else "موردی یافت نشد"
        report_parts.append(f"| **{category.capitalize()}** | {display_items} |")

    return "\n".join(report_parts)


def main(input_text:str):
    """
    Main function to run the extraction and summarization agents.

    This function initializes the OpenAI client, sets up the agents with their
    respective prompts, runs them on the input text, and saves the results
    to the output directory.
    """
    # --- Setup ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # --- Agent Initialization ---
    extractor = ExtractorAgent(client=client, prompt_path=EXTRACTOR_PROMPT_PATH)
    summarizer = SummarizerAgent(client=client, prompt_path=SUMMARIZER_PROMPT_PATH)

    # --- Execution ---
    print("⏳ Running agents on the input text...")

    # 1. Extract entities
    extracted_data = extractor.run(input_text)
    print("✅ Extraction complete.")

    # 2. Summarize text
    summary = summarizer.run(input_text)
    print("✅ Summarization complete.")

    # --- Output ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save raw outputs
    ENTITIES_OUTPUT_PATH.write_text(
        extracted_data.model_dump_json(indent=2),
        encoding="utf-8"
    )
    SUMMARY_OUTPUT_PATH.write_text(summary, encoding="utf-8")
    
    # Create and save Markdown report
    markdown_report = create_markdown_report(summary, extracted_data)
    MARKDOWN_REPORT_PATH.write_text(markdown_report, encoding="utf-8")
    
    print(f"\n🎉 All outputs saved successfully in '{OUTPUT_DIR}' directory.")
    print(f"📄 JSON: {ENTITIES_OUTPUT_PATH.name}, TXT: {SUMMARY_OUTPUT_PATH.name}, MD: {MARKDOWN_REPORT_PATH.name}")


if __name__ == "__main__":
    # --- CLI Setup ---
    parser = argparse.ArgumentParser(
        description="Extract entities and summarize text using AI agents.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Create a mutually exclusive group for text input
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t", "--text",
        type=str,
        help="Direct text input to process."
    )
    group.add_argument(
        "-f", "--file",
        type=Path,
        help="Path to a .txt file to process."
    )

    args = parser.parse_args()
    
    final_input_text = ""
    if args.text:
        print("Got text from --text argument.")
        final_input_text = args.text
    elif args.file:
        try:
            print(f"Reading text from file: {args.file}")
            final_input_text = args.file.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
            exit(1) # Exit with an error code
    else:
        print("No input provided. Using default sample text.")
        final_input_text = TEXT_INPUT

    # Run the main logic with the determined input text
    main(input_text=final_input_text)