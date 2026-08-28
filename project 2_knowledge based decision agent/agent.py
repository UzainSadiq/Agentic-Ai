from typing import TypedDict, List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from config import CHAT_MODEL, TOP_K, OPENROUTER_API_KEY, OPENROUTER_BASE_URL
from rag import retrieve

class AgentState(TypedDict, total=False):
    question: str; query_type: str; search_query: str; context: str; sources: List[Dict]; answer: str

llm=ChatOpenAI(model=CHAT_MODEL, temperature=0, api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, default_headers={'HTTP-Referer':'http://localhost:8501','X-Title':'Edu Agent'})

def analyze_query(state):
    prompt=f'''Classify this educational question as admission, course, scholarship, attendance, academic, or general. Also rewrite it for semantic search. Return exactly two lines: TYPE: <type> and SEARCH: <query>.\n\nUser question: {state["question"]}'''
    text=llm.invoke([HumanMessage(content=prompt)]).content.strip(); qt='general'; sq=state['question']
    for line in text.splitlines():
        if line.upper().startswith('TYPE:'): qt=line.split(':',1)[1].strip().lower()
        elif line.upper().startswith('SEARCH:'): sq=line.split(':',1)[1].strip()
    return {'query_type':qt,'search_query':sq or state['question']}

def retrieve_context(state):
    results=retrieve(state['search_query'],k=TOP_K); sources=[]; parts=[]
    for i,(doc,score) in enumerate(results,1):
        source=doc.metadata.get('source','unknown'); preview=' '.join(doc.page_content.split())
        sources.append({'source':source,'chunk':i,'score':round(float(score),4),'preview':preview[:220]+('...' if len(preview)>220 else '')})
        parts.append(f'[SOURCE {i}: {source}]\n{doc.page_content}')
    return {'context':'\n\n'.join(parts),'sources':sources}

def reason_and_answer(state):
    if not state.get('context','').strip(): return {'answer':'I could not find relevant information in the private knowledge base.'}
    prompt=f'''You are Edu Agent, a knowledge-based educational decision assistant. Answer only from the retrieved context. Do not invent university rules, fees, dates, or requirements. If information is missing, say so. Keep the answer clear and student-friendly.\n\nQuestion: {state['question']}\n\nRetrieved context:\n{state['context']}'''
    response=llm.invoke([SystemMessage(content='Be careful and evidence-grounded.'),HumanMessage(content=prompt)])
    return {'answer':response.content.strip()}

def build_graph():
    b=StateGraph(AgentState); b.add_node('query_analysis',analyze_query); b.add_node('retriever',retrieve_context); b.add_node('agent_reasoning',reason_and_answer); b.add_edge(START,'query_analysis'); b.add_edge('query_analysis','retriever'); b.add_edge('retriever','agent_reasoning'); b.add_edge('agent_reasoning',END); return b.compile()
graph=build_graph()
def run_agent(question):
    r=graph.invoke({'question':question}); return {'answer':r.get('answer','No answer generated.'),'query_type':r.get('query_type','general'),'sources':r.get('sources',[])}
