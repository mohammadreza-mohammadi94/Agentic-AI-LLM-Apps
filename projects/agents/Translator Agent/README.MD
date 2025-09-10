# English to Farsi Translator Agent

This project demonstrates a simple AI agent built with the `openai-agents` framework that translates English text into Farsi (Persian) using a GPT-4 based model.

## Features

- Uses a dedicated Translator Agent with clear instructions to provide concise and accurate English-to-Farsi translations.
- Ensures translation output is clean and free of additional or irrelevant text.
- Built with asynchronous execution for efficient processing.
- Uses Pydantic for structured output validation.


## Requirements

- Python 3.7+
- `openai-agents` package
- `python-dotenv` for environment variable management
- Valid OpenAI API key configured in `.env`


## Setup

1. Clone this repository.
2. Create a `.env` file in the project root with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ``` 

3. Install dependencies:

   ```bash
   pip install openai-agents python-dotenv pydantic
   ```


## Usage

Run the script to translate a sample English sentence into Farsi:

```bash
python translate_agent.py
```

Expected output:

```
من یک دانشمند داده متعهد و مهندس یادگیری ماشین با بیش از ۶ سال تجربه برنامه‌نویسی، شامل ۵ سال تخصص در یادگیری ماشین و یادگیری عمیق هستم.
```

## Code Highlights

* **Agent Definition**: The `TranslatorAgent` is instructed to produce accurate translations without extra text.
* **Output Model**: Uses a Pydantic `TranslationOutput` model to ensure the output format.
* **Execution**: Asynchronous main function runs the agent and prints the translation.


## Extending

* Easily adapt the agent for other language pairs by updating instructions.
* Integrate with larger multi-agent workflows.
* Extend output model for additional metadata or quality scores.

