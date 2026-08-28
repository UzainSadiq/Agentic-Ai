# 🤖 TeleAgent — Telegram Agentic AI Assistant

**Assignment:** Project 6 — Telegram Agentic AI Assistant  
**Stack:** Python + Streamlit + LangGraph + Telegram Bot + OpenRouter + local knowledge/tool layer

## 1. Project idea

TeleAgent is a Telegram chatbot where the user sends a normal-language request. Instead of simply forwarding the message to an LLM, the system uses an agent workflow:

**Telegram → LangGraph → Analyze → Tool/RAG → Validate → Generate → Telegram**

The agent can:
- answer normal questions through the LLM
- retrieve relevant information from a local knowledge base
- perform arithmetic with a safe calculator tool
- return current server time
- validate tool output before generating the final response

## 2. Why this is Agentic AI

The project demonstrates the important agentic concepts from the assignment:
- **Agent decision:** the workflow selects an action.
- **Tool use:** calculator and time tools can be executed.
- **Knowledge use:** local retrieval provides grounded evidence.
- **Stateful workflow:** LangGraph passes state through multiple nodes.
- **Validation:** a separate node checks the tool/RAG result.
- **Final generation:** OpenRouter generates the user-facing response.

## 3. API setup

This project uses **one AI API key: OpenRouter**.

The default model is:

`openrouter/free`

This is OpenRouter's free-model router. It automatically chooses among currently available free models.

Telegram also needs a **Telegram Bot Token** created with `@BotFather`. That token is for Telegram authentication, not an AI API.

## 4. Installation

### Windows

```powershell
cd telegram_agentic_ai_assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment

```powershell
copy .env.example .env
```

Open `.env` and add:

```env
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=openrouter/free
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Never commit `.env` to GitHub.

## 5. Run the Streamlit demo

```powershell
streamlit run app.py
```

The dashboard is designed for an instructor demonstration. It shows:
- system status
- agent playground
- agent workflow
- included tools
- project explanation
- agent trace

## 6. Run the Telegram bot

In another terminal:

```powershell
python telegram_bot.py
```

Open your bot in Telegram and send:

- `Explain LangGraph in simple words`
- `calculate (125 * 8) / 5`
- `what time is it?`
- `What is agentic AI?`

## 7. GitHub

Recommended repository name:

`telegram-agentic-ai-assistant`

Suggested description:

> A Telegram-based Agentic AI Assistant built with LangGraph, OpenRouter, tool calling, local RAG, and a modern Streamlit demonstration dashboard.

## 8. Folder structure

```text
telegram_agentic_ai_assistant/
│
├── app.py                 # attractive Streamlit instructor dashboard
├── agent.py               # LangGraph agent workflow
├── llm.py                 # OpenRouter API client
├── tools.py               # calculator, RAG, time tools
├── telegram_bot.py        # Telegram interface
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── knowledge_base.md
│
└── .streamlit/
    └── config.toml
```

## 9. Architecture

```text
                 ┌─────────────────┐
                 │  Telegram User  │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │  Telegram Bot   │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    LangGraph    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Analyze / Decide│
                 └────────┬────────┘
                          ↓
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        Calculator     Local RAG      Time
             └────────────┼────────────┘
                          ↓
                 ┌─────────────────┐
                 │    Validate     │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ OpenRouter LLM  │
                 │  Final Response │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Telegram Reply  │
                 └─────────────────┘
```

## 10. Instructor presentation script

> "This project is a Telegram Agentic AI Assistant. The key difference from a normal chatbot is that the system can decide what action is appropriate. LangGraph manages the workflow. Depending on the request, the agent can use a local knowledge source, calculator, or time tool. The result is validated, and then OpenRouter generates the final response. Telegram provides the user-facing interface, while Streamlit provides a visual dashboard for demonstration."

## 11. Important note

Free model availability and limits can change over time. If a free model is temporarily unavailable, change `OPENROUTER_MODEL` to another currently available free model from OpenRouter.
