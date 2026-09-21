from app.db.database import Base, engine
from app.db.models import Document, Chunk

Base.metadata.create_all(bind=engine)

print("Database tables created.")