# AI Text Processor: Extractor & Summarizer

A Python tool that uses AI to extract named entities and generate a summary from a given text. It's designed to be simple, efficient, and easy to use via a command-line interface.

-----

## ✨ Features

  * [cite\_start]**AI-Powered Summarization**: Condenses long texts into a two-paragraph summary[cite: 2].
  * [cite\_start]**Named Entity Extraction**: Identifies and categorizes entities like persons, organizations, and locations from the text[cite: 1].
  * **Command-Line Interface**: Run the tool directly from your terminal, providing text as a string or from a file.
  * **Multiple Output Formats**: Saves results as a plain text summary, a JSON file for entities, and a consolidated Markdown report.
  * **Customizable Prompts**: Easily modify the AI's behavior by editing simple text files.

-----

## 📂 Project Structure

The project is organized into logical folders for agents, prompts, and outputs.

```
.
├── .env                  # Stores your API key
├── main.py               # Main script with CLI logic
├── requirements.txt      # Project dependencies
├── sample_input.py       # Default text for processing
├── utils.py              # Helper functions
├── agents/
│   ├── extractor.py      # Agent for entity extraction
│   ├── summarizer.py     # Agent for summarization
│   └── schemas.py        # Pydantic models for data structure
└── prompts/
    ├── extractor_prompt.txt # Prompt for the extractor agent
    └── summarizer_prompt.txt  # Prompt for the summarizer agent
```

-----

## ⚙️ Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

  * Python 3.8 or newer
  * An [OpenAI API Key](https://platform.openai.com/api-keys)

### Step-by-Step Guide

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment**
    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install all required Python packages from the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your API Key**
    Create a file named `.env` in the project's root directory and add your OpenAI API key to it.

    ```env
    OPENAI_API_KEY="your-api-key-here"
    ```

-----

## ▶️ How to Run

You can run the script from your terminal in three different ways.

1.  **With the Default Text**
    Runs the process on the sample text provided in `sample_input.py`.

    ```bash
    python main.py
    ```

2.  **With a Text String**
    Processes a string of text provided directly in the command.

    ```bash
    python main.py --text "Your text to be processed goes here."
    ```

3.  **With a File**
    Processes the content of a specified text file.

    ```bash
    python main.py --file path/to/your/document.txt
    ```

-----

## 📄 Output Files

After a successful run, the results will be saved in the `output/` directory:

  * **`summary.txt`**: Contains the generated text summary.
  * **`entities.json`**: A JSON file with the list of extracted entities.
  * **`report.md`**: A well-formatted Markdown file containing both the summary and the entities in a table.

-----

## ✍️ Customizing Prompts

You can easily change the behavior of the AI agents by editing the prompt files located in the `prompts/` directory.