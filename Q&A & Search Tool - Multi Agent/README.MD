# 🧠 Q&A + Web Search Agent

This is a simple multi-agent system built using the OpenAI Agents SDK.  
It includes two agents working together:

## 🎯 Objective

Given a user query, the system:
1. Decides if the question requires a web search.
2. If **yes**, it searches the web and returns a summarized answer.
3. If **no**, it simply ends (you can later add a direct answer agent if needed).

---

## 🧩 Project Structure

```

project/
│
├── agents/
│   ├── decision\_agent.py     # Agent that returns YES/NO
│   ├── search\_agent.py       # Agent that performs web search and summarizes
│   └── models.py             # Shared Pydantic models
│
├── main.py                   # Runs the whole logic
├── .env                      # Your OpenAI API Key
└── requirements.txt          # Python dependencies

````

---

## 🚀 How to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt


2. **Set your OpenAI API key**
   Create a `.env` file:

   ```
   OPENAI_API_KEY=your_key_here
   ```

3. **Run the project**

   ```bash
   python main.py
   ```

---

## 🔧 Example Input

```
What are the top AI conferences in 2025?
```

### ✅ Possible Output

```
Decision Agent: YES  
Search Agent: A summary of top conferences like NeurIPS, ICLR, CVPR, etc.
```

---

## 📦 Requirements

* Python 3.9+
* `openai-agents` (official SDK)
* `python-dotenv`

---

## 📌 Notes

* The `decision_agent` only replies with `"YES"` or `"NO"`.
* The `search_agent` uses `WebSearchTool` for real-time lookup.
* You can extend this system by adding a direct-answer agent for "NO" cases.

