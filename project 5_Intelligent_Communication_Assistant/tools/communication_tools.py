import json
import os
from datetime import datetime
from pathlib import Path


LOG_PATH = Path("logs/actions.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _write_log(action: str, details: dict):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(
            f"[{timestamp}] {action}: {json.dumps(details, ensure_ascii=False)}\n"
        )


def send_email(
    recipient: str,
    subject: str,
    message: str,
) -> dict:
    """
    Sends an email when SendGrid is configured. Otherwise records a safe demo delivery.

    Args:
        recipient: Destination email address.
        subject: Email subject.
        message: Professional email body.
    """
    if not recipient:
        return {"success": False, "message": "Email recipient was not provided."}

    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("SENDGRID_FROM_EMAIL")

    if sendgrid_key and sender:
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            mail = Mail(
                from_email=sender,
                to_emails=recipient,
                subject=subject,
                plain_text_content=message,
            )
            response = SendGridAPIClient(sendgrid_key).send(mail)

            result = {
                "success": 200 <= response.status_code < 300,
                "message": f"SendGrid response: {response.status_code}",
                "mode": "sendgrid",
            }
            _write_log("send_email", {**result, "recipient": recipient, "subject": subject})
            return result
        except Exception as exc:
            result = {
                "success": False,
                "message": f"SendGrid failed: {exc}",
                "mode": "sendgrid",
            }
            _write_log("send_email", result)
            return result

    result = {
        "success": True,
        "message": f"Demo email recorded for {recipient}. Add SENDGRID_API_KEY and SENDGRID_FROM_EMAIL for real delivery.",
        "mode": "demo",
    }
    _write_log(
        "send_email",
        {"recipient": recipient, "subject": subject, "message": message, "mode": "demo"},
    )
    return result


def send_notification(
    title: str,
    message: str,
    priority: str = "normal",
) -> dict:
    """
    Sends a Pushover notification when configured. Otherwise records a safe demo notification.

    Args:
        title: Short notification title.
        message: Notification message.
        priority: normal, high, or emergency.
    """
    pushover_token = os.getenv("PUSHOVER_APP_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER_KEY")

    if pushover_token and pushover_user:
        try:
            import requests

            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": pushover_token,
                    "user": pushover_user,
                    "title": title,
                    "message": message,
                    "priority": 1 if priority.lower() == "high" else 0,
                },
                timeout=15,
            )
            response.raise_for_status()
            result = {
                "success": True,
                "message": "Pushover notification sent successfully.",
                "mode": "pushover",
            }
            _write_log("send_notification", {**result, "title": title})
            return result
        except Exception as exc:
            result = {
                "success": False,
                "message": f"Pushover failed: {exc}",
                "mode": "pushover",
            }
            _write_log("send_notification", result)
            return result

    result = {
        "success": True,
        "message": "Demo notification recorded. Add Pushover credentials for real delivery.",
        "mode": "demo",
    }
    _write_log(
        "send_notification",
        {"title": title, "message": message, "priority": priority, "mode": "demo"},
    )
    return result


def log_action(action: str, reason: str) -> dict:
    """
    Records the assistant's decision in the application log.

    Args:
        action: The selected communication action.
        reason: Short explanation for the decision.
    """
    result = {"success": True, "message": "Action recorded."}
    _write_log("agent_decision", {"action": action, "reason": reason})
    return result
