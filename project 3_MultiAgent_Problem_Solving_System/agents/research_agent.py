from langchain_core.prompts import ChatPromptTemplate
from config import get_llm
from prompts import RESEARCH_PROMPT
from tools.web_search import web_search

def research_agent(problem: str) -> str:
    llm = get_llm()

    # The agent gets a web-search observation first.
    search_notes = web_search(problem, max_results=5)

    prompt = ChatPromptTemplate.from_template(RESEARCH_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "problem": (
            f"{problem}\n\n"
            f"External research observations:\n{search_notes}"
        )
    })

    return response.content
