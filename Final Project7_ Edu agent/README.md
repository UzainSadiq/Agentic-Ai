# 🎓 EduAgent — Autonomous AI Student Success & Study Planner

EduAgent is an Agentic AI university study assistant built with Streamlit, LangChain,
LangGraph-backed agents, Groq, local RAG, web search and Google Sheets.

## Architecture

User → Streamlit → EduAgent Agent → Tool Selection
                                      ├─ Student/Planning tools
                                      ├─ Private Notes RAG
                                      ├─ Web Resource Search
                                      └─ Google Sheets
                                              ↓
                                         Final Response

## Features

- Personalized study planning
- Weak-subject prioritization
- Private course-note RAG
- Current web resource search
- Google Sheets study-session logging
- Google Sheets plan storage
- Streamlit multi-page UI
- Environment-variable based secrets
- Error handling and structured tool outputs

## 1. Create virtual environment

Windows PowerShell:

```powershell
cd "C:\agentic ai 2"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Then enter the project:

```powershell
cd "project1_intelligent ask agent\EduAgent"
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## 2. Configure Groq

Create `.env2` and set:

```text
GROQ_API_KEY=YOUR_NEW_KEY
GROQ_MODEL=openai/gpt-oss-20b
```

Do not commit `.env2`.

## 3. Build the RAG knowledge base

Run:

```powershell
python rag\ingest.py
```

The first run downloads the embedding model and creates `chroma_db/`.

Add your own lecture notes as `.txt` files inside `knowledge/`, then run the command again.

## 4. Google Sheets

Create a Google Cloud project, enable Google Sheets API and Google Drive API,
create a service account, download its JSON key and save it in the project as:

```text
google_credentials.json
```

Create a Google Sheet and share it with the service-account email as Editor.

Copy the spreadsheet ID into `.env2`:

```text
GOOGLE_SHEET_ID=...
```

Do not upload the service-account JSON to GitHub.

## 5. Test the agent

From the project folder:

```powershell
python -c "from agent import run_agent; print(run_agent('Create a 7-day study plan with 2 hours per day.'))"
```

Try:

```text
What are my weakest subjects?
Explain paging from my OS notes.
Find current LangGraph learning resources.
Record that I studied Operating Systems for 60 minutes.
Save my generated study plan to Google Sheets.
```

## 6. Run Streamlit

```powershell
streamlit run app.py
```

Open the Local URL shown by Streamlit.

## Important

This project uses a local web-search tool and local RAG. Tool execution happens in
your Python application. The model decides which available tool is useful, and the
tool returns structured information to the agent.

For a university demonstration, explain:
1. Why an agent is needed instead of a simple chatbot.
2. How tool selection works.
3. How RAG grounds answers in private notes.
4. How Google Sheets becomes an external action tool.
5. How environment variables protect API keys.
