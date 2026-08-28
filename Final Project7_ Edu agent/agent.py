import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from prompts import SYSTEM_PROMPT
from state import load_student
from tools.study_tools import get_student_overview, generate_study_plan, get_subject_details
from tools.sheets_tools import log_study_session, save_study_plan, get_recent_sessions
from tools.resource_tools import search_learning_resources
from rag.retriever import search_notes

load_dotenv(".env2")

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Put it in .env2.")

llm = ChatGroq(
    model=MODEL,
    api_key=API_KEY,
    temperature=0.2,
)

tools = [
    get_student_overview,
    get_subject_details,
    generate_study_plan,
    search_notes,
    search_learning_resources,
    log_study_session,
    save_study_plan,
    get_recent_sessions,
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

def run_agent(user_goal: str) -> str:
    student = load_student()
    enriched_goal = f"""
Student profile:
{student}

User request:
{user_goal}
"""
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": enriched_goal}
        ]
    })
    messages = result.get("messages", [])
    for message in reversed(messages):
        content = getattr(message, "content", None)
        if content:
            return content if isinstance(content, str) else str(content)
    return "I could not generate a response."

if __name__ == "__main__":
    print(run_agent("Create a 7-day study plan for me with 2 hours per day."))
