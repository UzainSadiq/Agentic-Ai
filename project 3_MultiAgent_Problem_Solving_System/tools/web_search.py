from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return short text results."""
    try:
        results = DDGS().text(query, max_results=max_results)
        results = list(results)

        if not results:
            return "No web results were found."

        lines = []
        for i, item in enumerate(results, 1):
            title = item.get("title", "Untitled")
            body = item.get("body", "")
            href = item.get("href", "")
            lines.append(f"{i}. {title}\n{body}\nSource: {href}")

        return "\n\n".join(lines)

    except Exception as e:
        return f"Web search failed: {e}"
