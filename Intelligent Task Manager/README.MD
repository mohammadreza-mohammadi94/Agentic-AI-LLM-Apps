# 🤖 Intelligent Task Manager

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)
[](https://platform.openai.com/)

An agentic AI system that intelligently manages a user's task list. The agent uses a Large Language Model (LLM) to analyze and prioritize tasks based on urgency and importance, then schedules them on a calendar using a robust, multi-step tool-calling process.

This project demonstrates a professional, modular architecture for building reliable AI agents that can automate complex decision-making and integrate with external APIs.

-----

## ✨ Key Features

  - **LLM-Powered Prioritization**: Leverages an LLM to understand the context of tasks and rank them intelligently.
  - **Multi-Step Agentic Workflow**: Uses a robust, two-step process (Prioritize -\> Schedule) for reliable and predictable behavior.
  - **Tool Calling**: Defines and uses custom tools for prioritizing tasks and scheduling them on a calendar.
  - **Mock API Integration**: Simulates scheduling tasks on an external calendar API, providing a template for real-world integration.
  - **Interactive UI**: A clean and simple Gradio interface allows users to input tasks via text or JSON file upload and view the results.
  - **Modular & Professional Codebase**: The project is structured into distinct modules for easy maintenance, testing, and extension.

-----

## 🖼️ Application Screenshot

<a href="https://ibb.co/ZzwL0Dzf"><img src="https://i.ibb.co/Qvqb4wvJ/image.png" alt="image" border="0"></a>

-----

## ⚙️ How It Works

The agent follows a strict, two-step process to ensure reliability:

1.  **Prioritization Step**: The agent first sends the user's raw task list to an LLM whose *only job* is to analyze the tasks and return a prioritized list of task names. This isolates the complex decision-making into one focused step.
2.  **Scheduling Step**: The agent then loops through the prioritized list. For each task, it makes a *separate* call to the LLM, instructing it to use the `schedule_task` tool. This Python-controlled loop ensures every task is processed correctly.

This decoupled approach is more robust than a single, complex prompt and is a best practice for building dependable AI agents.

-----

## 🔧 Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/intelligent-task-manager.git
cd intelligent-task-manager
```

### 2\. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

You will need an API key from OpenAI.

1.  Create a copy of the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your secret API key:
    ```env
    OPENAI_API_KEY="sk-..."
    ```

-----

## 🏃‍♀️ How to Run

Execute the main application script from the root directory to launch the Gradio interface:

```bash
python app.py
```

The script will start a local web server. Open the provided URL (e.g., `http://127.0.0.1:7860`) in your browser to interact with the task manager.

-----

## 📂 Project Structure

The project uses a modular structure to separate concerns:

```
/intelligent_task_manager
|
|-- app.py                      # Main Gradio application
|-- task_agent.py               # Core logic for the AI agent
|-- task_loader.py              # Loads tasks from a JSON file
|-- prompts.py                  # Stores and manages all system prompts
|-- config.py                   # Manages configuration and API keys
|
|-- tools/                      # Package for tools
|   |-- __init__.py
|   |-- definitions.py          # JSON schemas for the LLM
|   |-- implementations.py      # Python functions for the tools
|
|-- .env                        # (Private) Your secret API key
|-- requirements.txt            # Dependencies
|-- sample_tasks.json           # Sample task list
```