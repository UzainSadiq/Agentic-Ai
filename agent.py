import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools import TOOLS


# =========================================================
# LOAD .env2
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, ".env2")

load_dotenv(ENV_FILE)


# =========================================================
# CHECK API KEY
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Make sure .env2 exists and contains GROQ_API_KEY."
    )


# =========================================================
# CREATE LLM
# =========================================================
llm = ChatGroq(
model="openai/gpt-oss-safeguard-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)



# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are an intelligent task execution agent.

Your job is to understand the user's goal and decide whether
you need to use one or more tools.

Available tools:

1. calculator
   Use for mathematical calculations.

2. weather
   Use for current weather information.

3. web_search
   Use for internet searches and current external information.

Follow this process:

1. Understand the user's goal.
2. Decide what information or action is required.
3. Select the appropriate tool.
4. Execute the tool.
5. Observe the result.
6. If another tool is necessary, use it.
7. When enough information has been collected, provide
   a clear final answer.

Do not use a tool when it is unnecessary.

If a calculation is required, use the calculator tool instead
of calculating manually.

If weather information is requested, use the weather tool.

If the user asks for current or external information,
use the web_search tool.

Explain the final answer clearly and concisely.
"""


# =========================================================
# CREATE AGENT
# =========================================================

agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


# =========================================================
# FUNCTION USED BY STREAMLIT
# =========================================================

def run_agent(user_input: str):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        }
    )

    messages = result["messages"]

    final_message = messages[-1]

    content = final_message.content

    if isinstance(content, str):
        return content

    # Handle newer content-block responses
    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, dict):

                if block.get("type") == "text":
                    text_parts.append(
                        block.get("text", "")
                    )

            elif isinstance(block, str):
                text_parts.append(block)

        return "\n".join(text_parts)

    return str(content)