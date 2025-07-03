# /app.py
import gradio as gr
import json
from task_agent import TaskManagerAgent
from task_loader import load_tasks_from_json
from config import TASKS_FILE_PATH

agent = TaskManagerAgent()

def run_task_manager(tasks_input):
    """Handles the Gradio button click."""
    if not tasks_input:
        return "Please provide a task list in JSON format.", ""
    
    try:
        # Check if input is a file path (from upload) or raw text
        if hasattr(tasks_input, 'name'):
             tasks = load_tasks_from_json(tasks_input.name)
        else:
            tasks = json.loads(tasks_input)
        
        if not tasks:
            return "Could not load or parse tasks.", ""
            
        summary, logs = agent.process_tasks(tasks)
        
        # Format logs for display
        log_string = "\n".join(logs)
        
        return summary, log_string
    except json.JSONDecodeError:
        return "Invalid JSON format. Please check your input.", ""
    except Exception as e:
        return f"An error occurred: {e}", ""

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft(), title="Intelligent Task Manager") as demo:
    gr.Markdown("# 🤖 Intelligent Task Manager")
    gr.Markdown("Provide your tasks in JSON format or upload a file. The agent will prioritize and schedule them.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Input Tasks")
            # Load sample tasks as default
            with open(TASKS_FILE_PATH, 'r') as f:
                sample_tasks = f.read()
            task_input_box = gr.Textbox(lines=10, label="Tasks (JSON format)", value=sample_tasks)
            upload_button = gr.UploadButton("Or Upload JSON File", file_types=[".json"])
            process_button = gr.Button("Process Tasks", variant="primary")

        with gr.Column():
            gr.Markdown("### Agent Output")
            summary_output = gr.Textbox(label="Final Summary", interactive=False)
            logs_output = gr.Textbox(label="Scheduling Logs", lines=10, interactive=False)
    
    # Wire up the components
    process_button.click(
        fn=run_task_manager,
        inputs=[task_input_box],
        outputs=[summary_output, logs_output]
    )
    
    upload_button.upload(
        fn=run_task_manager,
        inputs=[upload_button],
        outputs=[summary_output, logs_output]
    )

if __name__ == "__main__":
    demo.launch()