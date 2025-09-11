# Cerebras Debate Orchestrator

A multi-agent system that simulates a structured, formal debate between different AI personas on a given topic, powered by models on the Cerebras Cloud. The entire debate is orchestrated and automatically saved as a formatted Markdown transcript.

## 📜 Overview

This project sets up a debate with multiple AI agents, each with a distinct persona and powered by a specific LLM. The debate follows a formal structure:

1.  **Round 1: Opening Statements**: Each agent presents its initial position.
2.  **Round 2: Cross-Examination**: Agents take turns asking questions to one another.
3.  **Final Round: Judgment**: Each agent, stepping out of its persona, acts as an impartial judge to vote for the winner (without voting for itself) and justifies its decision.

The orchestrator manages the turn-taking, provides the correct context to each agent, and compiles the full conversation into a clean transcript.

## ✨ Features

-   **Multi-Agent Simulation**: Orchestrates a debate between multiple AI agents.
-   **Structured Debate Format**: Follows a clear, multi-round structure for a coherent discussion.
-   **Customizable Personas**: Easily define agent roles, perspectives, and models in `src/config.py`.
-   **Cerebras Integration**: Leverages various models available through the Cerebras Cloud API.
-   **Automatic Transcript Generation**: Saves the complete debate in a readable Markdown file with a timestamp.

## ⚙️ How It Works

The `DebateManager` class in `src/debate_manager.py` is the core orchestrator.

1.  It loads the agent configurations and debate topic from `src/config.py`.
2.  It proceeds through the rounds, calling the Cerebras API for each agent's turn via the `get_cerebras_response` function in `src/llm_interface.py`.
3.  It maintains a `conversation_log` to provide historical context for each new AI generation.
4.  After the debate concludes, it saves the entire transcript to a Markdown file (e.g., `debate_transcript_YYYYMMDD_HHMMSS.md`).

## 🚀 Getting Started

### 1. Prerequisites

-   Python 3.7+
-   A Cerebras Cloud API key.

### 2. Installation

1.  Navigate to the project directory:
    ```bash
    cd projects/multi-agent/Cerebras-Debate-Orchestrator
    ```

2.  Create a `requirements.txt` file in this directory with the following content:
    ```txt
    cerebras-cloud-sdk
    python-dotenv
    ```

3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. API Key Configuration

For security, avoid hardcoding API keys. Use an environment variable instead.

1.  Create a file named `.env` in the `Cerebras-Debate-Orchestrator` directory.
2.  Add your Cerebras API key to the `.env` file:
    ```
    CEREBRAS_API_KEY="your-api-key-here"
    ```
3.  The suggested code change for `src/llm_interface.py` (see below) will automatically and securely load this key.

## 🏃‍♀️ Usage

1.  **(Optional) Customize the Debate**:
    Open `src/config.py` to change the `DEBATE_TOPIC`, modify agent personas, or assign different Cerebras models.

2.  **Run the Debate**:
    Execute the main script from the `Cerebras-Debate-Orchestrator` directory:
    ```bash
    python src/debate_manager.py
    ```

3.  **View the Output**:
    The script will print the debate to the console in real-time. Once finished, a new Markdown file named `debate_transcript_[timestamp].md` will be created in the same directory.

## 📂 Project Structure

```
Cerebras-Debate-Orchestrator/
├── src/
│   ├── config.py             # Agent personas, models, and debate topic
│   ├── debate_manager.py     # Main orchestration logic
│   └── llm_interface.py      # Handles communication with Cerebras API
│
├── .env                      # Stores your API key (you create this)
├── requirements.txt          # Project dependencies (you create this)
├── debate_transcript_...md   # Example output file
└── README.md                 # This file
```