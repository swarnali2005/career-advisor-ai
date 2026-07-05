from app.graph.graph_builder import build_graph

graph = build_graph()

initial_state = {
    "user_message": "hi",
    "conversation_history": [],
    "is_distress": None,
    "affect": None,
    "extracted_profile": None,
    "retrieved_careers": None,
    "explanation": None,
    "final_response": None,
}

result = graph.invoke(initial_state)

print("is_distress:", result.get("is_distress"))
print("Response:", result["final_response"])