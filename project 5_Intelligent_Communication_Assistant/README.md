# Intelligent Communication Assistant

Agentic AI Project 5 based on the assignment brief:

> Build an agent that analyzes information and prepares or sends appropriate communications or notifications according to defined conditions.

## What this project demonstrates

- Streamlit UI
- Gemini LLM agent
- Custom function/tool calling
- Email automation tool
- Push notification tool
- Confirmation and action logging
- Decision making based on request conditions

## Architecture

```text
USER
  |
  v
STREAMLIT UI
  |
  v
GEMINI AGENT
(Analyze situation / decision making)
  |
  +---------> send_email
  |
  +---------> send_notification
  |
  +---------> log_action
  |
  v
CONFIRMATION + ACTION LOG
  |
  v
STREAMLIT STATUS UI
```

## API key

The core AI agent requires only:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

The project uses Google's official `google-genai` SDK.

SendGrid and Pushover credentials are optional. If they are not configured, the application runs in **Demo Mode**: the tool calls still execute locally and are recorded in `logs/actions.log`, but no real message is sent.

## Setup — Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and add your Google Gemini API key.

Run:

```bash
streamlit run app.py
```

## Optional real delivery

### SendGrid

Add:

```env
SENDGRID_API_KEY=...
SENDGRID_FROM_EMAIL=your_verified_sender@example.com
```

### Pushover

Add:

```env
PUSHOVER_APP_TOKEN=...
PUSHOVER_USER_KEY=...
```

Without these values, Demo Mode remains active.

## Teacher demo

Try these requests:

1. `Send an email to student@example.com reminding them that the project is due tomorrow.`
2. `Send me a high-priority notification that the project deadline is tomorrow.`
3. `Send an email to student@example.com and a notification because the deadline is tomorrow.`

The Gemini agent decides which custom tool(s) to call. The tool executes locally, returns a result to the agent, and the application displays confirmation and logs.

## Security

Never commit `.env` or real API keys to GitHub or submit them in an assignment ZIP.
