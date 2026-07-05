from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph.graph_builder import build_graph

app = FastAPI(title="Explainable Affect-Aware Career Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


class AdviceRequest(BaseModel):
    message: str
    history: list = []


class AdviceResponse(BaseModel):
    affect: str | None = None
    extracted_profile: dict | None = None
    retrieved_careers: list | None = None
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/advise", response_model=AdviceResponse)
def advise(request: AdviceRequest):
    initial_state = {
        "user_message": request.message,
        "conversation_history": request.history,
        "is_distress": None,
        "affect": None,
        "extracted_profile": None,
        "retrieved_careers": None,
        "explanation": None,
        "final_response": None,
    }

    result = graph.invoke(initial_state)

    return AdviceResponse(
        affect=result.get("affect"),
        extracted_profile=result.get("extracted_profile"),
        retrieved_careers=result.get("retrieved_careers"),
        response=result["final_response"],
    )