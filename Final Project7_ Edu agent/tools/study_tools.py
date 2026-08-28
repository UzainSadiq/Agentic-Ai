import json
from datetime import datetime
from pathlib import Path
from typing import List
from langchain_core.tools import tool

BASE_DIR = Path(__file__).resolve().parents[1]

def _load_student():
    with open(BASE_DIR / "data" / "student.json", "r", encoding="utf-8") as f:
        return json.load(f)

@tool
def get_student_overview() -> str:
    """Return the student's subjects, mastery, goals and assessment dates."""
    student = _load_student()
    rows = [
        f"{s['name']} ({s['code']}): mastery={s['mastery']}%, exam={s['exam_date']}, credits={s['credits']}"
        for s in student["subjects"]
    ]
    return (
        f"Student: {student['name']}\n"
        f"Program: {student['program']}\n"
        f"Semester: {student['semester']}\n"
        f"Weekly goal: {student['weekly_goal_hours']} hours\n"
        + "\n".join(rows)
    )

@tool
def get_subject_details(subject_name: str) -> str:
    """Get detailed information for one subject by name or code."""
    student = _load_student()
    q = subject_name.lower()
    for s in student["subjects"]:
        if q in s["name"].lower() or q == s["code"].lower():
            return json.dumps(s, indent=2)
    return f"Subject '{subject_name}' was not found."

@tool
def generate_study_plan(days: int = 7, hours_per_day: float = 2.0) -> str:
    """
    Generate a deterministic study plan. Prioritizes low mastery and nearer exams.
    Returns JSON so the agent can reason over structured data.
    """
    days = max(1, min(days, 30))
    hours_per_day = max(0.5, min(hours_per_day, 12.0))
    student = _load_student()
    subjects = student["subjects"]

    def score(s):
        # Higher score = higher priority.
        mastery_need = 100 - s["mastery"]
        exam_bonus = 0
        try:
            exam = datetime.strptime(s["exam_date"], "%Y-%m-%d").date()
            delta = (exam - datetime.now().date()).days
            if delta <= 14:
                exam_bonus = 40
            elif delta <= 30:
                exam_bonus = 20
        except ValueError:
            pass
        return mastery_need + exam_bonus + s.get("priority_weight", 1) * 5

    ranked = sorted(subjects, key=score, reverse=True)
    plan = []
    for day in range(1, days + 1):
        remaining = hours_per_day
        slots = []
        idx = (day - 1) % len(ranked)
        while remaining > 0.01:
            s = ranked[idx % len(ranked)]
            duration = min(1.0, remaining)
            activity = "Active recall + practice questions" if s["mastery"] < 70 else "Revision + timed practice"
            slots.append({
                "day": day,
                "subject": s["name"],
                "duration_hours": round(duration, 2),
                "activity": activity,
                "outcome": f"Improve {s['name']} mastery through focused practice."
            })
            remaining -= duration
            idx += 1
        plan.extend(slots)

    return json.dumps({
        "days": days,
        "hours_per_day": hours_per_day,
        "plan": plan
    }, indent=2)
