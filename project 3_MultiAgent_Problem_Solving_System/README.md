# 🤖 Multi-Agent Problem Solving System

A polished beginner-friendly **multi-agent AI project** using Streamlit + LangGraph + OpenRouter.

## 🔐 One API key only

This version is intentionally configured for **OpenRouter only**. You do not need a Groq key or OpenAI key.

Create a file named `.env` beside `app.py`:

```env
OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

The app uses OpenRouter's `openrouter/free` router, which selects an available free model automatically.

## 🧩 Agent architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Agent A: Research  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │  Agent B: Analysis  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Agent C: Execution  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Supervisor Agent    │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Final Answer      │
                    └─────────────────────┘
```

## ✨ Features

- OpenRouter only — one API key
- OpenRouter Free Router (`openrouter/free`)
- LangGraph multi-agent workflow
- Research + web search
- Analysis and comparison
- Practical execution planning
- Supervisor synthesis
- Modern Streamlit UI
- Agent cards and workflow tabs
- Demo prompts in the sidebar
- Clear session button
- API-key validation and friendly errors
- No secret stored in Python source code

## 🚀 Run in VS Code

### 1. Open the project

Open this folder in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env` and replace the placeholder with your OpenRouter key.

### 5. Start the app

```powershell
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, normally `http://localhost:8501`.

## 🧪 Suggested demo

Try:

> Compare AWS, Azure Cloud and Google Cloud for deployment of an AI application. Consider cost, scalability, services, ease of deployment, security, and recommend the best option for a university project.

## 🔒 Security

Never commit `.env` to GitHub. The `.gitignore` file already excludes it.

## 📚 Main technologies

- Python
- Streamlit
- LangGraph
- LangChain
- OpenRouter
- DDGS web search
