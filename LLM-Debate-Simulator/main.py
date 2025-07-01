# /main.py
"""
This file ties everything together. Its job is to define the models, 
run the simulator, and store and display the results.
"""

from debate_simulator import DebateSimulator
from utils import save_to_json, format_markdown_output, save_markdown_file
from ui import display_in_terminal, create_gradio_interface
from config import RANKED_DEBATE_FILE, DEBATE_SUMMARY_FILE

def main():
    """
    Main function to run the LLM Debate Simulator.
    """
    # 1. Setup: Define debaters and judge
    # You can easily swap models here.
    # Ensure the models/providers match what's configured in llm_clients.py
    debaters = [
            {
                "provider": "groq", 
                "model": "llama3-8b-8192", 
                "stance": "pro"
            },
            {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "stance": "con"
            },
            {
                "provider": "groq",
                "model": "llama3-70b-8192",
                "stance": "neutral"
            }
    ]
    
    judge = {
        "provider": "openai", 
        "model": "gpt-4o-mini"
            }

    # 2. Implementation: Run the simulation
    simulator = DebateSimulator(debaters, judge)
    
    # Run the debate to get arguments
    debate_arguments = simulator.run_debate()
    
    # Have the judge evaluate the arguments
    ranked_results = simulator.evaluate_debate()

    if "error" in ranked_results:
        print(f"Halting due to evaluation error: {ranked_results['error']}")
        return

    # 3. Deliverables: Save results to files
    save_to_json(ranked_results, RANKED_DEBATE_FILE)
    
    # 4. Visualization: Format and display output
    markdown_output = format_markdown_output(debate_arguments, ranked_results)
    
    save_markdown_file(markdown_output, DEBATE_SUMMARY_FILE)
    
    # Display in terminal
    display_in_terminal(markdown_output)

    # Optional: Launch Gradio interface for a richer view
    # To enable, uncomment the line below
    # create_gradio_interface(markdown_output)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
