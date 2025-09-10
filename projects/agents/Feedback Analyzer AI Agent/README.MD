# AI Customer Feedback Analyzer

This project is a command-line tool that uses AI to analyze customer feedback. It identifies the sentiment and core problem in a message and then generates a professional, empathetic response suggestion.

-----

## ✨ Features

  * **Sentiment Analysis**: Automatically determines if feedback is **positive**, **negative**, or **neutral**. [cite: 3]
  * **Problem Summarization**: Distills customer feedback into a single, concise sentence identifying the main issue. [cite: 3]
  * **AI-Powered Responses**: Generates a ready-to-use, professional response draft based on the analyzed problem. [cite: 2]
  * **Command-Line Interface**: Easy to use directly from your terminal with text or file inputs.
  * **Structured Output**: Saves the full analysis and suggested reply in both `JSON` and `Markdown` formats.

-----

## 📂 Project Structure

```
.
├── .env
├── main.py
├── requirements.txt
├── utils.py
├── agts/
│   ├── analyzer.py
│   ├── responder.py
│   └── schemas.py
└── prompts/
    ├── analyzer_prompt.txt
    └── responder_prompt.txt
```

-----

## 🔧 Prerequisites

  * Python 3.8+
  * An [OpenAI API Key](https://platform.openai.com/api-keys)

-----

## ⚙️ Installation

1.  **Clone the Repository**

    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment** (Recommended)

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Create `requirements.txt`**
    Create a file named `requirements.txt` and add the following lines:

    ```
    openai
    pydantic
    python-dotenv
    ```

4.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Environment File**
    Create a file named `.env` in the main project folder and add your API key:

    ```
    OPENAI_API_KEY="your-api-key-here"
    ```

-----

## ▶️ How to Run

The script must be run with an input. You can provide it directly or via a file.

  * **Provide text directly:**

    ```bash
    python main.py --text "Your customer's feedback message goes here."
    ```

    **Example:**

    ```bash
    python main.py --text "The new user interface is very slow and confusing."
    ```

  * **Provide a text file:**

    ```bash
    python main.py --file path/to/your/feedback.txt
    ```

-----

## 📄 Output

The results are saved in the `output/` directory:

  * **`final_report.json`**: A JSON file containing the original feedback, the full analysis, and the suggested response.
  * **`report.md`**: A well-formatted Markdown file for easy reading of the complete report.

-----

## ✍️ Customization

You can easily change the AI's behavior by editing the prompt files in the `prompts/` directory.

  * **`analyzer_prompt.txt`**: Modify this to change how feedback is analyzed.
  * **`responder_prompt.txt`**: Modify this to change the tone, style, or structure of the generated responses.