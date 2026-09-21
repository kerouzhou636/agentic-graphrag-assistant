from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.neo4j import driver

from pydantic import BaseModel
from app.db.models import Document

from app.retrieval.vector_search import search_similar_chunks

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }


@router.get("/neo4j-test")
def neo4j_test():
    driver.verify_connectivity()

    return {
        "neo4j": "connected",
    }

class DocumentCreate(BaseModel):
    title: str
    content: str


@router.post("/")
def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
):
    document = Document(
        title=document_data.title,
        content=document_data.content,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "title": document.title,
    }
@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()

    return [
        {
            "id": document.id,
            "title": document.title,
            "content": document.content,
        }
        for document in documents
    ]
class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@router.post("/search")
def search_documents(request: SearchRequest):
    return search_similar_chunks(
        query=request.query,
        limit=request.limit,
    )