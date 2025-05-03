from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base  # Ensure this is correct based on your models

# Replace with your actual database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Example for SQLite; change this accordingly.

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
