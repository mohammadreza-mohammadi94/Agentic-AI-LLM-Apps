# 🤖 Intelligent Sales Email Automation

This project implements a **multi-agent system** for automating the creation, refinement, and sending of cold sales emails using the `openai-agents` SDK.

## 🚀 How It Works

* **Sales Manager Agent** oversees the workflow
* **Three Writer Agents** (Professional, Engaging, Busy) generate drafts in different styles
* **Email Manager Agent** handles subject generation, HTML formatting, and (mock) sending

The agents collaborate to produce high-quality, persona-tailored sales emails with minimal human input.

## 🛠️ Requirements

```bash
pip install openai-agents sendgrid python-dotenv
```

Add your API keys to a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
SENDGRID_API_KEY=your_sendgrid_key
```

## ▶️ Usage

```bash
python sales_email_automation.py
```

The system will generate and (mock) send a sales email based on the user’s request.

---

Let me know if you want to turn this into a deployable API or web UI.
