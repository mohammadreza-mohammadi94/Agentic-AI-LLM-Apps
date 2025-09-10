# ShopSmart Assistant

ShopSmart Assistant is an AI-powered customer support chatbot for an e-commerce platform selling electronics. It uses OpenAI's GPT-4o-mini model to provide empathetic and professional responses to customer inquiries, logs issues to a JSONL file, and sends urgent notifications via Pushover. The chatbot runs on a Gradio web interface, making it easy to interact with customers locally.

## Project Overview

The assistant handles customer support tasks, such as troubleshooting product issues, processing refund requests, and escalating urgent cases. Key features include:
- **AI Responses**: Generates helpful responses using OpenAI's GPT-4o-mini.
- **Issue Logging**: Saves customer issues (e.g., customer ID, description, urgency) to `customer_issues.jsonl`.
- **Urgent Notifications**: Sends alerts for urgent issues (e.g., "urgent" or "emergency") via Pushover.
- **Gradio Interface**: Provides a browser-based chat interface at `http://127.0.0.1:7860`.
- **Logging**: Records events and errors in `shopsmart_assistant.log` for debugging.

## Project Structure

```
ShopSmart Assistant/
├── shopsmart_assistant.py  # Main chatbot script
├── logger.py              # Custom logging module
├── prompts.json           # System prompt configuration
├── .env                   # API keys (OpenAI, Pushover)
├── shopsmart_assistant.log # Runtime logs (generated)
├── customer_issues.jsonl  # Customer issue logs (generated)
└── README.md              # This file
```

## Requirements

- **Python**: 3.8 or higher.
- **API Keys**:
  - OpenAI API key (https://platform.openai.com/account/api-keys).
  - Pushover User Key and Application Token (https://pushover.net, optional).

## Setup
1. **Set Up Virtual Environment**:
   ```bash
   python -m venv ai
   .\ai\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv requests gradio
   ```

3. **Configure .env File**:
   - Create `.env` in the project directory:
     ```
     OPENAI_API_KEY=your_openai_api_key
     PUSHOVER_USER=your_pushover_user_key
     PUSHOVER_TOKEN=your_pushover_app_token
     ```
   - Get keys from https://platform.openai.com and https://pushover.net.

4. **Verify Files**:
   - Ensure `main.py`, `logger.py`, and `prompts.json` are present.
   - The script creates `customer_issues.jsonl` and `shopsmart_assistant.log` automatically.

## Usage

1. **Run the Chatbot**:
   ```bash
   python shopsmart_assistant.py
   ```
   - The Gradio interface starts at `http://127.0.0.1:7860`.
   - A startup notification is sent via Pushover or logged locally.

2. **Interact via Browser**:
   - Open `http://127.0.0.1:7860` in a browser.
   - Enter inquiries like:
     - “Urgent: My TV arrived damaged!”
     - “My laptop won’t charge.”
     - “I need a refund for order #12345.”

3. **Check Logs**:
   - **Runtime Logs**: `shopsmart_assistant.log` for events and errors.
   - **Issues**: `customer_issues.jsonl` for logged customer issues, e.g.:
     ```json
     {"timestamp": "2025-07-01T04:20:05", "customer_id": "user123", "issue_description": "TV arrived damaged", "urgency": "high"}
     ```

4. **Stop the Chatbot**:
   - Press `Ctrl+C` in the terminal.
S
