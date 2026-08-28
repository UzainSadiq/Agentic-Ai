from typing import TypedDict, Any, List, Dict

class StudentState(TypedDict, total=False):
    user_goal: str
    student: Dict[str, Any]
    relevant_notes: str
    plan: List[Dict[str, Any]]
    tool_results: List[str]
    final_answer: str

def load_student() -> Dict[str, Any]:
    import json
    from pathlib import Path
    path = Path(__file__).parent / "data" / "student.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
