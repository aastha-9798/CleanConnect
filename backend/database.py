from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base , Session

DB_url="sqlite:///./backend/auth.db"
engine = create_engine(DB_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db(): # Dependency to get a database session
    db = SessionLocal() # Create a new database session
    try:
        yield db   # Yield the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use