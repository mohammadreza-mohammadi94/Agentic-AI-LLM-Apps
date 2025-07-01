# /utils.py
"""
Helper functions used in different parts of the project are located here.
"""
import json
import os

def save_to_json(data, filepath):
    """
    Saves a dictionary to a JSON file with pretty printing.

    Args:
        data (Dict[str, Any]): The dictionary to save.
        filepath (str): The path to the output JSON file.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully saved ranked results to {filepath}")
    except IOError as e:
        print(f"Error: Could not write to file: {filepath}. {e}")

def format_markdown_output(debate_args, ranked_results):
    """
    Formats the complete debate and evaluation into a Markdown string.

    Args:
        debate_args (Dict[str, Dict[str, str]]): The arguments from the debaters.
        ranked_results (Dict[str, Any]): The JSON results from the judge.

    Returns:
        str: A formatted Markdown string.
    """
    from config import DEBATE_TOPIC
    output = f"# 🤖 LLM Debate Simulation\n\n"
    output += f"## Topic: *{DEBATE_TOPIC}*\n\n"
    output += "---\n\n"
    
    output += "### 🏆 Judge's Final Ranking\n\n"
    output += "| Rank | Debater | Stance | Model Used | Judge's Reasoning |\n"
    output += "|:----:|:--------|:-------|:-----------|:------------------|\n"
    
    ranking = sorted(ranked_results['ranking'], key=lambda x: x['rank'])
    
    for item in ranking:
        output += f"| **{item['rank']}** | {item['debater']} | {item['stance'].capitalize()} | `{item['model']}` | {item['reasoning']} |\n"
        
    output += "\n---\n\n"
    
    output += "### 💬 Full Arguments\n\n"
    for debater_name, info in debate_args.items():
        output += f"#### Argument from {debater_name} (`{info['stance']}` stance, using `{info['model']}`)\n"
        # Perform the replacement outside the f-string for compatibility
        formatted_argument = info['argument'].replace('\n', '\n> ')
        # Now, use the new variable in the f-string
        output += f"> {formatted_argument}\n\n"
        
    return output

def save_markdown_file(content, filepath):
    """
    Saves a string content to a text file.

    Args:
        content (str): The string content to save.
        filepath (str): The path to the output file.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully saved debate summary to {filepath}")
    except IOError as e:
        print(f"Error: Could not write to file {filepath}. {e}")