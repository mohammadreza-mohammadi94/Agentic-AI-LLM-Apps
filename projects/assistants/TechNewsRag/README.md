# TechNews RAG Assistant

This project is a RAG (Retrieval-Augmented Generation) application that allows you to ask questions about recent tech news articles.

## Features

- Load articles from different tech news websites.
- Ask questions in natural language.
- Get answers based on the content of the articles.
- Filter answers by source.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd TechNewsRag
    ```
3.  Install the project in editable mode:
    ```bash
    pip install -e .
    ```
4.  Create a `.env` file and add your `OPENAI_API_KEY`:
    ```
    OPENAI_API_KEY="your-api-key"
    ```

## Usage

After installation, you can run the application using the command-line script:

```bash
technews-rag
```

Alternatively, you can run it as a python module:

```bash
python -m src.main
```

The application will prompt you to ask a question and choose a source to search for answers.

```
Ask a question about the articles (type 'q' to quit.): What is OpenAI's latest acquisition?

Available sources to filter by:
1. KD Nuggets
2. Tech Crunch
3. All
Choose a source number [1-3]: 3
```

The assistant will then provide an answer based on the selected articles.
```
--- Answer ---
OpenAI has acquired a company called Sky, which is an AI interface for Mac.
--- End of Answer ---
```