import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


def chat(prompt: str, temperature: float = 0.2) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Add it to .env or your deployment secrets."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "TeleAgent Agentic AI Assistant",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a reliable agentic AI assistant. Follow the requested format exactly when asked.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error {response.status_code}: {response.text[:500]}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
