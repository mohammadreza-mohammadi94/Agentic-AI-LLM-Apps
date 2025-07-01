# /ui.py
"""
This module is responsible for displaying the output. 
Here, both methods of displaying in the terminal and 
creating a simple user interface with Gradio are implemented.
"""

import gradio as gr

def display_in_terminal(markdown_content):
    """
    Prints the formatted Markdown content directly to the terminal.

    Args:
        markdown_content (str): The Markdown string to be displayed.
    """
    print("\n" + "="*80)
    print("Debate Simulation Results")
    print("="*80 + "\n")
    print(markdown_content)

def create_gradio_interface(markdown_content):
    """
    Creates and launches a Gradio interface to display the debate results.

    Args:
        markdown_content (str): The Markdown string to display in the interface.
    """
    with gr.Blocks(theme=gr.themes.Soft(), title="LLM Debate Simulator") as demo:
        gr.Markdown("# 🤖 LLM Debate Simulation Results")
        gr.Markdown(markdown_content)

    print("\n🚀 Launching Gradio interface...")
    print("Please open the following URL in your browser.")
    demo.launch()
