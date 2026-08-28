from langgraph.graph import StateGraph, START, END

from state import AgentState
from agents.research_agent import research_agent
from agents.analysis_agent import analysis_agent
from agents.execution_agent import execution_agent
from agents.supervisor_agent import supervisor_agent


def research_node(state: AgentState):
    result = research_agent(state["problem"])
    return {
        "research": result,
        "supervisor_log": state.get("supervisor_log", [])
        + ["Supervisor → Agent A (Research) completed."]
    }


def analysis_node(state: AgentState):
    result = analysis_agent(state["problem"], state["research"])
    return {
        "analysis": result,
        "supervisor_log": state.get("supervisor_log", [])
        + ["Supervisor → Agent B (Analysis) completed."]
    }


def execution_node(state: AgentState):
    result = execution_agent(
        state["problem"],
        state["research"],
        state["analysis"],
    )
    return {
        "execution": result,
        "supervisor_log": state.get("supervisor_log", [])
        + ["Supervisor → Agent C (Execution) completed."]
    }


def supervisor_node(state: AgentState):
    result = supervisor_agent(
        state["problem"],
        state["research"],
        state["analysis"],
        state["execution"],
    )
    return {
        "final_answer": result,
        "supervisor_log": state.get("supervisor_log", [])
        + ["Supervisor combined all agent outputs."]
    }


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("execution", execution_node)
    workflow.add_node("supervisor", supervisor_node)

    workflow.add_edge(START, "research")
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "execution")
    workflow.add_edge("execution", "supervisor")
    workflow.add_edge("supervisor", END)

    return workflow.compile()


graph = build_graph()


def run_problem(problem: str):
    initial_state: AgentState = {
        "problem": problem,
        "supervisor_log": [],
    }
    return graph.invoke(initial_state)
