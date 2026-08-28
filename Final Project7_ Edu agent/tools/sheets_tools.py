import os
import json
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool

SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "EduAgent Study Tracker")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "google_credentials.json")

def _get_worksheet(tab_name: str):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as e:
        raise RuntimeError("Install gspread and google-auth first.") from e

    if not Path(CREDENTIALS_FILE).exists():
        raise FileNotFoundError(
            f"{CREDENTIALS_FILE} not found. Create a Google service-account key and share the spreadsheet with its service-account email."
        )

    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not spreadsheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID is missing in .env2.")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)

    try:
        return sh.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        return sh.add_worksheet(title=tab_name, rows=1000, cols=12)

@tool
def log_study_session(subject: str, duration_minutes: int, activity: str, outcome: str = "") -> str:
    """Record a completed study session in the Google Sheet."""
    ws = _get_worksheet("Study Sessions")
    if not ws.get_all_values():
        ws.append_row(["Timestamp", "Subject", "Duration (min)", "Activity", "Outcome"])
    ws.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        subject,
        int(duration_minutes),
        activity,
        outcome,
    ])
    return f"Study session saved: {subject}, {duration_minutes} minutes."

@tool
def save_study_plan(plan_json: str) -> str:
    """Save a generated JSON study plan into the Google Sheet."""
    ws = _get_worksheet("Study Plans")
    if not ws.get_all_values():
        ws.append_row(["Saved At", "Plan JSON"])
    ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M"), plan_json])
    return "Study plan saved successfully to Google Sheets."

@tool
def get_recent_sessions(limit: int = 10) -> str:
    """Read recent study sessions from Google Sheets."""
    ws = _get_worksheet("Study Sessions")
    values = ws.get_all_values()
    if len(values) <= 1:
        return "No study sessions have been recorded yet."
    rows = values[-max(1, min(limit, 50)):]
    return json.dumps(rows, indent=2)
