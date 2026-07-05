from app.graph.graph_builder import build_graph

graph = build_graph()

test_messages = [
    "I have no idea what I'm doing with my life, everything feels overwhelming, but I do enjoy working with numbers",
    "I'm pretty confident I want to go into software engineering",
    "I can't decide between medicine and engineering, both seem equally good",
    "I don't really understand what a data analyst actually does day to day",
]

for msg in test_messages:
    print(f"\n{'='*80}\nMessage: {msg}\n{'='*80}")
    initial_state = {
        "user_message": msg,
        "conversation_history": [],
        "is_distress": None,
        "affect": None,
        "extracted_profile": None,
        "retrieved_careers": None,
        "explanation": None,
        "final_response": None,
    }
    result = graph.invoke(initial_state)
    print(f"[Detected affect: {result['affect']}]\n")
    print(result["final_response"])