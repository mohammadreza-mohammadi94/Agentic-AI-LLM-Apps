# 🚀 AgenticAI

A comprehensive multi-agent AI framework featuring specialized agents with guardrails, built for real-world automation tasks (e.g., resume analysis, sales outreach, word counting).

---

## ⚙️ Architecture Highlights

* **Agentic Orchestration**: Manager agents direct specialist agents as tools, enabling clear multi-step workflows.
* **Guardrails**: Input validation layers that prevent privacy violations and unsafe inputs.
* **Multi-LLM Integration**: Easily plug in different providers for redundancy and performance optimization.
* **Modular & Extendable**: Projects share reusable agent-building patterns, guardrail designs, and runner logic using `openai-agents`.

---

## 🛠️ Getting Started

```bash
git clone https://github.com/mohammadreza-mohammadi94/AgenticAI.git
cd AgenticAI/<your-subproject>
pip install -r requirements.txt
# Add `.env` file with keys: OPENAI_API_KEY, SENDGRID_API_KEY, etc.
python <script_name>.py
```

---

## 📂 Projects
<!-- PROJECTS-INDEX-START -->

# Project index

## agents

- [Data Extractor Agent](projects/agents/Data%20Extractor%20Agent)
- [Extractor and Summarizer Agent](projects/agents/Extractor%20and%20Summarizer%20Agent) - # AI Text Processor: Extractor & Summarizer
- [Feedback Analyzer AI Agent](projects/agents/Feedback%20Analyzer%20AI%20Agent) - # AI Customer Feedback Analyzer
- [Financial Researcher - SerperAPI and OpenAI](projects/agents/Financial%20Researcher%20-%20SerperAPI%20and%20OpenAI) - # FinancialResearcher Crew
- [Image Analyzer Agent - AutoGen](projects/agents/Image%20Analyzer%20Agent%20-%20AutoGen) - # Multi-Modal Image Analyzer Agent
- [InsightBot](projects/agents/InsightBot) - Analytical Chatbot
- [Intelligent Resume Analyst](projects/agents/Intelligent%20Resume%20Analyst) - # Intelligent Resume Analyst
- [Intelligent Task Manager](projects/agents/Intelligent%20Task%20Manager) - # 🤖 Intelligent Task Manager
- [Planner And Executor Agent](projects/agents/Planner%20And%20Executor%20Agent)
- [Sales Email Automation - OpenAI SDK](projects/agents/Sales%20Email%20Automation%20-%20OpenAI%20SDK) - # 🤖 Intelligent Sales Email Automation
- [Summarizer Agent](projects/agents/Summarizer%20Agent) - # 🧠 LLM-Based Word Counter & Summarizer
- [Translator Agent](projects/agents/Translator%20Agent) - # English to Farsi Translator Agent


## assistants

- [Shop-Smart-Assistant(OpenAI)](projects/assistants/Shop-Smart-Assistant%28OpenAI%29) - # ShopSmart Assistant
- [Smart Home Assistant](projects/assistants/Smart%20Home%20Assistant)


## demos

- [LangChain-PDFChat](projects/demos/LangChain-PDFChat)
- [Simple Agent ChatBot - Streamlit & T5](projects/demos/Simple%20Agent%20ChatBot%20-%20Streamlit%20%26%20T5)


## experiments

- [Dynamic-Agent Creation & Simulation Word - AutoGen](projects/experiments/Dynamic-Agent%20Creation%20%26%20Simulation%20Word%20-%20AutoGen) - # Multi-Agent Simulation World
- [LLM-Debate-Simulator](projects/experiments/LLM-Debate-Simulator) - # 🤖 LLM Debate Simulator


## market-research

- [AI Market Sentiment Analyzer](projects/market-research/AI%20Market%20Sentiment%20Analyzer)
- [AI Product Research Agent](projects/market-research/AI%20Product%20Research%20Agent)
- [SentimentAnalysis For Text-LangChain-Streamlit](projects/market-research/SentimentAnalysis%20For%20Text-LangChain-Streamlit)
- [Stock Reasercher and Picker \[CrewAI\]](projects/market-research/Stock%20Reasercher%20and%20Picker%20%5BCrewAI%5D) - # StockPicker Crew


## multi-agent

- [AI Engineer Team](projects/multi-agent/AI%20Engineer%20Team) - # EngTeam Crew
- [Automated Market Research Agent System](projects/multi-agent/Automated%20Market%20Research%20Agent%20System) - # Automated Market Research Agent System
- [Q&A & Search Tool - Multi Agent](projects/multi-agent/Q%26A%20%26%20Search%20Tool%20-%20Multi%20Agent) - # 🧠 Q&A + Web Search Agent


## tools

- [DeepSearch - OpenAI SDK](projects/tools/DeepSearch%20-%20OpenAI%20SDK)
- [Tool-Augmented Chain with Calculator](projects/tools/Tool-Augmented%20Chain%20with%20Calculator)


## utilities

- [ScriptGenerator](projects/utilities/ScriptGenerator)

<!-- PROJECTS-INDEX-END -->


## 🌟 Why AgenticAI?

* Achieve **safe, multi-stage automation** with minimal code.
* Design **flexible agent workflows**, combining GPT-powered toolkits with domain guardrails.
* Deploy production-grade AI pipelines across HR, sales, analytics, and more.

---

## 📚 Next Steps

* Add real email sending via SendGrid or SMTP
* Deploy as APIs or conversational bots
* Integrate custom datasets and retrieval agents
* Improve guardrails for broader compliance enforcement

---

**AgenticAI** equips you to build safe, modular, and powerful AI workflows—no need to reinvent orchestration or alignment logic. Enjoy experimenting!
