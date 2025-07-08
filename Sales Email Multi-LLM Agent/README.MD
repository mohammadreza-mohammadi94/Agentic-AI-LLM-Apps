# 💼 Multi-Agent SDR Email Automation System

This project implements a **multi-agent sales email automation system** that drafts, refines, and sends cold emails using multiple LLMs and guardrails to ensure quality and privacy.

## 🧠 Features

* **Hierarchical agent architecture** with manager and writer agents
* **Multi-LLM support**: DeepSeek, Google Gemini, Groq, and OpenAI
* **Guardrail system** that blocks inputs containing personal names
* **Automated email generation** with professional, engaging, and concise personas

## ⚙️ Requirements

Install dependencies:

```bash
pip install openai-agents python-dotenv sendgrid pydantic
```

Create a `.env` file with the following keys:

```env
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
DEEPSEEK_API_KEY=...
GROQ_API_KEY=...
SENDGRID_API_KEY=...
```

## 🚀 Usage

Run the system:

```bash
python agent.py
```

It will:

* Block unsafe prompts with names (via a guardrail)
* Generate 3 versions of a cold sales email
* Select and print the best one

## 🔒 Safety

Includes a built-in input guardrail using a dedicated agent to detect personal names and reject unsafe inputs.

