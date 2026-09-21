from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(
    title="Agentic GraphRAG Knowledge Assistant",
    description="A knowledge assistant using agentic vector and graph retrieval.",
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}