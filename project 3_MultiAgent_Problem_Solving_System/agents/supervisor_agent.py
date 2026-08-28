from langchain_core.prompts import ChatPromptTemplate
from config import get_llm
from prompts import SUPERVISOR_PROMPT

def supervisor_agent(
    problem: str,
    research: str,
    analysis: str,
    execution: str,
) -> str:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(SUPERVISOR_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "problem": problem,
        "research": research,
        "analysis": analysis,
        "execution": execution,
    })
    return response.content
