from typing import TypedDict

class AgentState(TypedDict, total=False):
    problem: str
    research: str
    analysis: str
    execution: str
    supervisor_log: list[str]
    final_answer: str
