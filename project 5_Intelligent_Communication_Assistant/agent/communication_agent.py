import os
from datetime import datetime

from google import genai
from google.genai import types

from tools.communication_tools import (
    send_email,
    send_notification,
    log_action,
)


class CommunicationAgent:
    """Gemini-powered decision agent using custom function calling."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add your Google Gemini API key to .env."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

        self.tools = [
            send_email,
            send_notification,
            log_action,
        ]

    def run(self, request: str, recipient: str = "", priority: str = "Normal"):
        prompt = f"""
You are an intelligent communication assistant.

Analyze the user's communication request and decide what action is appropriate.

Available actions:
1. send_email — use when an email is explicitly requested or is the clearest channel.
2. send_notification — use for short, urgent or immediate notifications.
3. log_action — always record what the assistant decided and why.

Rules:
- Never invent a recipient email.
- If an email is requested but no email address is available, do not call send_email.
- For urgent/immediate requests, a notification is appropriate.
- The user may request both email and notification.
- Keep messages professional and concise.
- Execute the appropriate tools using function calling.

User request:
{request}

Provided recipient:
{recipient or "Not provided"}

Priority:
{priority}

Current time:
{datetime.now().isoformat(timespec="seconds")}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                ),
                temperature=0.2,
            ),
        )

        tool_calls = []
        if getattr(response, "automatic_function_calling_history", None):
            history = response.automatic_function_calling_history
            # Keep a compact trace for the UI. Actual function execution is handled by the SDK.
            for item in history:
                if hasattr(item, "parts"):
                    for part in item.parts:
                        if getattr(part, "function_call", None):
                            call = part.function_call
                            tool_calls.append(getattr(call, "name", "tool"))

        decision = self._infer_decision(tool_calls, response.text)
        logs = self._read_recent_logs()

        actions = []
        for tool_name in dict.fromkeys(tool_calls):
            actions.append({
                "tool": tool_name,
                "success": True,
                "message": "Tool executed by Gemini automatic function calling.",
            })

        if not actions:
            actions.append({
                "tool": "log_action",
                "success": True,
                "message": "No external delivery tool was required; request was logged.",
            })

        return {
            "decision": decision,
            "reason": response.text.strip(),
            "actions": actions,
            "confirmation": "The request was analyzed and the selected action was processed. Check the action log for the execution trace.",
            "logs": logs,
        }

    @staticmethod
    def _infer_decision(tool_calls, text):
        names = set(tool_calls)
        if "send_email" in names and "send_notification" in names:
            return "email_and_notification"
        if "send_email" in names:
            return "send_email"
        if "send_notification" in names:
            return "send_notification"
        return "log_only"

    @staticmethod
    def _read_recent_logs():
        path = "logs/actions.log"
        if not os.path.exists(path):
            return ["No actions logged yet."]
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.rstrip() for line in lines[-12:]]
