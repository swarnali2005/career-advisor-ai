from langgraph.graph import StateGraph, END
from .state import AdvisorState
from .nodes import (
    detect_affect,
    extract_profile,
    retrieve_careers,
    generate_explanation,
    compose_response
)

def build_graph():
    graph = StateGraph(AdvisorState)

    graph.add_node("detect_affect", detect_affect)
    graph.add_node("extract_profile", extract_profile)
    graph.add_node("retrieve_careers", retrieve_careers)
    graph.add_node("generate_explanation", generate_explanation)
    graph.add_node("compose_response", compose_response)

    graph.set_entry_point("detect_affect")
    graph.add_edge("detect_affect", "extract_profile")
    graph.add_edge("extract_profile", "retrieve_careers")
    graph.add_edge("retrieve_careers", "generate_explanation")
    graph.add_edge("generate_explanation", "compose_response")
    graph.add_edge("compose_response", END)

    return graph.compile()