# main orchestration
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI

from agts.analyzer import FeedbackAnalyzerAgent
from agts.responder import ResponseGeneratorAgent
from agts.schemas import AnalysisResult, FinalReport

#----------------#
# Configuration  #
#----------------#
load_dotenv()

# Define Directories
PROMPTS_DIR = Path('prompts')
OUTPUT_DIR = Path("output")
ANALYZER_AGENT_PROMPT = PROMPTS_DIR / "analyzer_prompt.txt"
RESPONDER_AGENT_PROMPT = PROMPTS_DIR / "responder_prompt.txt"

# Define Output File
MARKDOWN_REPORT_PATH = OUTPUT_DIR / "report.md"
FINAL_REPORT_JSON_PATH = OUTPUT_DIR / "final_report.json"

def create_markdown_report(report: FinalReport) -> str:
    report_parts = []
    
    # --- Customer Feedback ---
    report_parts.append("## 📩 Customer Feedback")
    formatted_feedback = report.original_feedback.replace('\n', '\n> ')
    report_parts.append(f"> {formatted_feedback}")
    report_parts.append("\n---\n")

    # --- Sentiment Analysis ---
    report_parts.append("## ⚙️ Sentiment Analysis")
    report_parts.append(f"- **Tone (Sentiment):** `{report.analysis.sentiment.capitalize()}`")
    report_parts.append(f"- **Problem Summary:** {report.analysis.problem_summary}")
    report_parts.append("\n---\n")

    # -- Response Recommendation ---
    report_parts.append("## 📝 Recommended Response")
    report_parts.append(report.suggested_response)

    return "\n".join(report_parts)


def main(input_text:str):
    # --- Setup ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # --- Agent Initialization ---
    analyzer = FeedbackAnalyzerAgent(client=client, 
                                     prompt_path=ANALYZER_AGENT_PROMPT)
    responder = ResponseGeneratorAgent(client=client, 
                                       prompt_path=RESPONDER_AGENT_PROMPT)
    
    # Execution
    print("⏳ Running feedback analysis pipeline...")

    # Get analysis from the first agent
    analysis_result = analyzer.run(input_text)
    print("✅ Analysis Complete.")

    # Get response from the second agent using the problem summary
    suggested_response = responder.run(
        problem_summary=analysis_result.problem_summary
    )
    print("✅ Response Generated.")

    # Final Report Generation
    final_report = FinalReport(
        original_feedback=input_text,
        analysis=analysis_result,
        suggested_response=suggested_response
    )

    # Output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save the full report as JSON
    FINAL_REPORT_JSON_PATH.write_text(
        final_report.model_dump_json(indent=2),
        encoding="utf-8"
    )

    # Create and save Markdown report
    markdown_content = create_markdown_report(final_report)
    MARKDOWN_REPORT_PATH.write_text(markdown_content, encoding="utf-8")


if __name__ == "__main__":
     # --- CLI Setup ---
    parser = argparse.ArgumentParser(
        description="Get sentiment and a suggested response from Customer Feedback.",
        formatter_class=argparse.RawTextHelpFormatter
    )

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
    
    # Determine the input text
    final_input_text = ""
    if args.text:
        print("Processing text from --text argument.")
        final_input_text = args.text
    elif args.file:
        try:
            print(f"Processing text from file: {args.file}")
            final_input_text = args.file.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
            exit(1)

    if not final_input_text:
        print("No input provided. Please use --text or --file to provide an input.")
        parser.print_help()
        exit(1)
    # Run the main logic
    main(input_text=final_input_text)