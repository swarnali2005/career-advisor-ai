from app.graph.graph_builder import build_graph

graph = build_graph()

initial_state = {
    "user_message": "I don't really understand what a data analyst actually does day to day",
    "conversation_history": [],
    "affect": None,
    "extracted_profile": None,
    "retrieved_careers": None,
    "explanation": None,
    "final_response": None,
}

result = graph.invoke(initial_state)
print("Extracted profile:", result["extracted_profile"])
print("Detected affect:", result["affect"])
print("Response:", result["final_response"])