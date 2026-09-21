from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Chunk, Document
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import generate_embedding


def process_document(document_id: int):
    db: Session = SessionLocal()

    try:
        document = db.get(Document, document_id)

        if document is None:
            raise ValueError(f"Document {document_id} not found")

        chunks = chunk_text(document.content)

        for chunk_content in chunks:
            embedding = generate_embedding(chunk_content)

            chunk = Chunk(
                document_id=document.id,
                content=chunk_content,
                embedding=embedding,
            )

            db.add(chunk)

        db.commit()

        print(
            f"Created {len(chunks)} embedded chunks "
            f"for document {document.title}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    process_document(1)