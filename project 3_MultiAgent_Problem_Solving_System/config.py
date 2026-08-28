"""Central configuration for the Multi-Agent Problem Solving System.

This project intentionally uses ONE provider and ONE secret:
OPENROUTER_API_KEY.
"""

import os
from dotenv import load_dotenv

# Load local environment files. Only OPENROUTER_API_KEY is required.
load_dotenv(".env")
load_dotenv(".env2")  # backwards-compatible with older project copies

PROVIDER = "openrouter"
MODEL_NAME = "openrouter/free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def require_openrouter_key() -> str:
    value = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not value:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Create a .env file and add:\n\n"
            "OPENROUTER_API_KEY=sk-or-v1-your_key_here"
        )
    return value


def get_llm():
    """Return an OpenRouter-backed LangChain chat model."""
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=MODEL_NAME,
        base_url=OPENROUTER_BASE_URL,
        api_key=require_openrouter_key(),
        temperature=0.2,
        max_retries=2,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Multi-Agent Problem Solving System",
        },
    )
