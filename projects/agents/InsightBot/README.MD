Analytical Chatbot
A professional, modular LangChain-based chatbot that answers questions and creates visualizations using Cohere (or flan-t5-base), Tavily Search, and PythonREPL.
Features

Modular architecture with separate modules for config, LLM, tools, agent, and UI.
Streamlit UI for user interaction and visualization display.
Supports Cohere or free flan-t5-base model.
Tools: Tavily Search (web search) and PythonREPL (code execution).
Logging and error handling.
Unit tests for tools and agent.

Installation

Create and activate a Conda environment:
conda create -n langchain_env_new python=3.9
conda activate langchain_env_new


Install dependencies:
pip install -r requirements.txt


Set up environment variables: Create a .env file in the project root:
COHERE_API_KEY=your_cohere_api_key
TAVILY_API_KEY=your_tavily_api_key


Run the chatbot:
streamlit run main.py



Usage

Open the Streamlit UI in your browser.
Ask questions like:
"Plot the number of employees at the top 3 tech companies in 2024."
"What is the capital of France?"


For plots, check the outputs/plot.png file or view in the UI.

Project Structure
analytical_chatbot/
├── src/                # Source code
├── tests/              # Unit tests
├── .env                # Environment variables
├── requirements.txt    # Dependencies
├── main.py             # Entry point
├── README.md           # Documentation
└── agent.log           # Logs

Running Tests
pytest tests/

Contributing

Fork the repository.
Create a feature branch.
Submit a pull request.

License
MIT License
