from datetime import datetime
from pathlib import Path
import ast
import operator as op
import re

KB_PATH = Path(__file__).parent / "data" / "knowledge_base.md"


# Safe arithmetic evaluator: only numbers and arithmetic operators.
_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculator(query: str) -> str:
    candidates = re.findall(r"[\d\s\+\-\*\/\%\(\)\.\^]+", query)
    expression = max(candidates, key=len).strip() if candidates else ""
    expression = expression.replace("^", "**")
    if not expression or not re.search(r"\d", expression):
        return "Calculator could not find a valid arithmetic expression."
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree)
        return f"Calculator result: {result}"
    except Exception as exc:
        return f"Calculator error: {exc}"


def knowledge_search(query: str, max_chunks: int = 3) -> str:
    text = KB_PATH.read_text(encoding="utf-8")
    chunks = [c.strip() for c in text.split("\n## ") if c.strip()]
    terms = set(re.findall(r"[a-zA-Z0-9]{3,}", query.lower()))
    scored = []
    for chunk in chunks:
        lower = chunk.lower()
        score = sum(1 for term in terms if term in lower)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    chosen = [chunk for score, chunk in scored[:max_chunks] if score > 0]
    if not chosen:
        return "No strongly matching local knowledge was found."
    return "\n\n".join(chosen)


def current_time() -> str:
    return datetime.now().astimezone().strftime(
        "Current server time: %Y-%m-%d %H:%M:%S %Z"
    )
