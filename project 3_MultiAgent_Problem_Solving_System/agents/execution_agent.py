from langchain_core.prompts import ChatPromptTemplate
from config import get_llm
from prompts import EXECUTION_PROMPT

def execution_agent(problem: str, research: str, analysis: str) -> str:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(EXECUTION_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "problem": problem,
        "research": research,
        "analysis": analysis,
    })
    return response.content
