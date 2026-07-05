from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph.graph_builder import build_graph

app = FastAPI(title="Explainable Affect-Aware Career Advisor")

# Allow the Streamlit frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for development; restrict this before real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


class AdviceRequest(BaseModel):
    message: str


class AdviceResponse(BaseModel):
    affect: str
    extracted_profile: dict
    retrieved_careers: list
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/advise", response_model=AdviceResponse)
def advise(request: AdviceRequest):
    initial_state = {
        "user_message": request.message,
        "conversation_history": [],
        "affect": None,
        "extracted_profile": None,
        "retrieved_careers": None,
        "explanation": None,
        "final_response": None,
    }

    result = graph.invoke(initial_state)

    return AdviceResponse(
        affect=result["affect"],
        extracted_profile=result["extracted_profile"],
        retrieved_careers=result["retrieved_careers"],
        response=result["final_response"],
    )