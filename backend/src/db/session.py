from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.base import Base

# Engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

