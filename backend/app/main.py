from fastapi import FastAPI

app = FastAPI(
    title="Agentic GraphRAG Knowledge Assistant",
    description="A knowledge assistant using agentic vector and graph retrieval.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}