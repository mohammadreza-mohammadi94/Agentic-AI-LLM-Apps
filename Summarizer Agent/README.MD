# 🧠 LLM-Based Word Counter & Summarizer

This project uses **two AI agents** to (1) summarize a text and (2) count words — all powered by **prompt engineering with LLMs**.

## ✨ Features

* 📄 **Summarization Agent**: Generates a concise summary (max 300 words).
* 🔢 **Word Count Agent**: Counts words in the original and summarized text using a prompt-based LLM.
* ✅ Uses [OpenAI Agents SDK](https://github.com/openai/openai-agents) with `gpt-4o-mini`.

## 📦 Requirements

```bash
pip install openai-agents python-dotenv pydantic
```

Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=your-api-key
```

## 🚀 Usage

1. Put your input text inside the file:

   ```
   file_path = '<YOUR_FILE_PATH>'
   ```

2. Run the script:

```bash
python your_script_name.py
```

3. Output includes:

   * Original word count
   * Summary (max 300 words)
   * Word count of the summary
