from langchain_core.prompts import ChatPromptTemplate
from config import get_llm
from prompts import ANALYSIS_PROMPT

def analysis_agent(problem: str, research: str) -> str:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(ANALYSIS_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "problem": problem,
        "research": research,
    })
    return response.content
