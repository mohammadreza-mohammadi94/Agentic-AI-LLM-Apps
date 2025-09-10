# /app.py
"""This file ties everything together into a user-facing Gradio application."""

import gradio as gr
import os
from career_advisor import CareerAdvisor
from file_processor import extract_text_from_pdf

# Instantiate the advisor
advisor_instance = CareerAdvisor()

def process_resume_and_question(pdf_file, question, chat_history, resume_state):
    """
    Main function to handle Gradio chat interactions.
    """
    # 1. Process PDF if it's newly uploaded
    if pdf_file is not None and resume_state is None:
        chat_history.append({"role": "assistant", "content": f"Thank you for uploading `{pdf_file.name}`. What can I help you with?"})
        resume_text = extract_text_from_pdf(pdf_file)
        if resume_text is None or "Could not extract" in resume_text:
            chat_history.append({"role": "assistant", "content": "Sorry, I couldn't read your resume. Please try another PDF."})
            return chat_history, None
        return chat_history, resume_text

    # 2. Handle questions if resume has been processed
    if resume_state is not None:
        if not question:
            chat_history.append({"role": "assistant", "content": "Please ask me a question about your career goals."})
            return chat_history, resume_state

        chat_history.append({"role": "user", "content": question})
        response = advisor_instance.get_advice(resume_state, question)
        chat_history.append({"role": "assistant", "content": response})
        return chat_history, resume_state

    # 3. Handle case where user asks a question without uploading a resume first
    if question:
        chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": "Please upload your resume first so I can provide tailored advice."})
    return chat_history, None


# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft(), title="AI Career Advisor") as demo:
    gr.Markdown("# 🤖 AI Career Advisor")
    gr.Markdown("Upload your resume (PDF), then ask a question to get personalized career advice.")

    # Stores the extracted resume text in a hidden state
    resume_text_state = gr.State(None)

    with gr.Row():
        with gr.Column(scale=1):
            pdf_upload = gr.File(label="Upload Your Resume (PDF)", file_types=[".pdf"])
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Conversation", type="messages")
            question_box = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What software engineering roles are a good fit for me?",
                interactive=True
            )
            # Submit action for the textbox
            question_box.submit(
                fn=process_resume_and_question,
                inputs=[pdf_upload, question_box, chatbot, resume_text_state],
                outputs=[chatbot, resume_text_state]
            )
            # Clear the textbox after submission
            question_box.submit(fn=lambda: "", inputs=[], outputs=[question_box])


if __name__ == "__main__":
    demo.launch()