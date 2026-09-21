from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Chunk
from app.ingestion.embeddings import generate_embedding


def search_similar_chunks(
    query: str,
    limit: int = 5,
):
    db = SessionLocal()

    try:
        query_embedding = generate_embedding(query)

        distance = Chunk.embedding.cosine_distance(query_embedding)

        statement = (
            select(Chunk, distance.label("distance"))
            .where(Chunk.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
        )

        results = db.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "distance": float(distance),
            }
            for chunk, distance in results
        ]

    finally:
        db.close()