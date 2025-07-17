# Automated Market Research Agent System

This project uses a multi-agent AI system to automate market research, report generation, and email delivery using `openai-agents`.

---

## 💡 What It Does

Given a high-level goal like _"Create a market analysis report of LLM providers in 2025"_, this system:

1. **Plans** the research steps.
2. **Searches** for insights (simulated).
3. **Writes** a Markdown report.
4. **Converts** the report to HTML.
5. **Emails** the final report.

---

## 🧠 Agent Roles

- **Planner Agent**: Breaks down the goal into actionable steps.
- **Search Agent**: Simulates web research.
- **Report Writer Agent**: Drafts a structured Markdown report.
- **Emailer Agent**: Converts the report to HTML and sends it via email.

---

## 🛠 Setup

1. Install dependencies:

```bash
pip install openai-agents python-dotenv markdown2 pydantic
````

2. Create a `.env` file and set your API key:

```env
OPENAI_API_KEY=your_openai_key_here
```

---

## ▶️ Run

```bash
python main.py
```

You’ll get:

* A clear research plan
* A multi-step agent execution log
* A generated email sent with the research report

---

## 🔧 Notes

* Web search and email sending are simulated (mock tools).
* Easily extend with real APIs like Tavily, Google Search, or SendGrid.


