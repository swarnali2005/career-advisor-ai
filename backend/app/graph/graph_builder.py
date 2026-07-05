from langgraph.graph import StateGraph, END
from .state import AdvisorState
from .nodes import (
    check_for_distress,
    detect_affect,
    extract_profile,
    retrieve_careers,
    generate_explanation,
    compose_response
)


def distress_response(state: AdvisorState) -> AdvisorState:
    state["final_response"] = (
        "It sounds like you might be going through something really difficult right now, "
        "and I want you to know that matters more than any career question. I'm not the right "
        "kind of support for this — please consider reaching out to someone who can help directly.\n\n"
        "If you're in India, you can call the **KIRAN Mental Health Helpline at 1800-599-0019** "
        "(toll-free, 24/7), or talk to a counselor, doctor, or someone you trust.\n\n"
        "I'll be here for career questions whenever you're ready — there's no rush."
    )
    return state


def route_after_distress_check(state: AdvisorState) -> str:
    return "distress_response" if state.get("is_distress") else "detect_affect"


def build_graph():
    graph = StateGraph(AdvisorState)

    graph.add_node("check_for_distress", check_for_distress)
    graph.add_node("distress_response", distress_response)
    graph.add_node("detect_affect", detect_affect)
    graph.add_node("extract_profile", extract_profile)
    graph.add_node("retrieve_careers", retrieve_careers)
    graph.add_node("generate_explanation", generate_explanation)
    graph.add_node("compose_response", compose_response)

    graph.set_entry_point("check_for_distress")

    graph.add_conditional_edges(
        "check_for_distress",
        route_after_distress_check,
        {
            "distress_response": "distress_response",
            "detect_affect": "detect_affect"
        }
    )

    graph.add_edge("distress_response", END)
    graph.add_edge("detect_affect", "extract_profile")
    graph.add_edge("extract_profile", "retrieve_careers")
    graph.add_edge("retrieve_careers", "generate_explanation")
    graph.add_edge("generate_explanation", "compose_response")
    graph.add_edge("compose_response", END)

    return graph.compile()