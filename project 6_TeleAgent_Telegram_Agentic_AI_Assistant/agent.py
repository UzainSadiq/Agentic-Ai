from typing import TypedDict, Optional
import json
import re
from langgraph.graph import StateGraph, START, END

from llm import chat
from tools import calculator, knowledge_search, current_time


class AgentState(TypedDict, total=False):
    user_query: str
    action: str
    tool: str
    evidence: str
    validation: str
    answer: str


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"action": "direct"}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"action": "direct"}


def analyze(state: AgentState) -> AgentState:
    prompt = f"""
You are the router for an agentic assistant.
Choose exactly one action for this user request:
- calculator: arithmetic/calculation is needed
- knowledge: the answer can be grounded in the local knowledge base
- time: current date/time is requested
- direct: normal conversational answer

Return ONLY JSON with keys action and reason.
User request: {state['user_query']}
"""
    decision = _extract_json(chat(prompt, temperature=0))
    action = decision.get("action", "direct")
    if action not in {"calculator", "knowledge", "time", "direct"}:
        action = "direct"
    return {"action": action, "tool": action if action != "direct" else "none"}


def execute(state: AgentState) -> AgentState:
    action = state["action"]
    query = state["user_query"]

    if action == "calculator":
        evidence = calculator(query)
    elif action == "knowledge":
        evidence = knowledge_search(query)
    elif action == "time":
        evidence = current_time()
    else:
        evidence = ""

    return {"evidence": evidence}


def validate(state: AgentState) -> AgentState:
    if state["action"] == "direct":
        return {"validation": "No external evidence required."}
    evidence = state.get("evidence", "").strip()
    if not evidence:
        return {"validation": "Tool returned no evidence; answer cautiously."}
    return {"validation": "Evidence received and ready for response generation."}


def generate(state: AgentState) -> AgentState:
    evidence = state.get("evidence", "")
    prompt = f"""
You are TeleAgent, a helpful Telegram agentic AI assistant.
Answer the user's request clearly and concisely.

User request:
{state['user_query']}

Agent action:
{state['action']}

Tool/evidence:
{evidence if evidence else 'No external tool was needed.'}

Validation:
{state.get('validation', '')}

Rules:
- If evidence is provided, use it and do not invent conflicting facts.
- If evidence is missing, say what is uncertain instead of pretending a tool succeeded.
- Keep the response suitable for Telegram.
"""
    return {"answer": chat(prompt, temperature=0.3)}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("analyze", analyze)
    graph.add_node("execute", execute)
    graph.add_node("validate", validate)
    graph.add_node("generate", generate)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "execute")
    graph.add_edge("execute", "validate")
    graph.add_edge("validate", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


GRAPH = build_graph()


def run_agent(user_query: str) -> dict:
    result = GRAPH.invoke({"user_query": user_query})
    return result
