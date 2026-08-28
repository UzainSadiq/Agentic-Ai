from langchain_core.tools import tool

@tool
def search_learning_resources(query: str, max_results: int = 5) -> str:
    """
    Search the web for current educational resources.
    Uses the ddgs package locally so the agent controls the tool execution.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        return "Resource search unavailable. Install the 'ddgs' package."

    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body"),
                })
        if not results:
            return "No web resources found."
        return str(results)
    except Exception as e:
        return f"Web search failed: {e}"
