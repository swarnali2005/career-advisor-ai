from fastapi import FastAPI

app = FastAPI(title="Explainable Affect-Aware Career Advisor")

@app.get("/health")
def health():
    return {"status": "ok"}