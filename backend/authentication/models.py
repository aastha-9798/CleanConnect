from sqlalchemy import Column, String
from backend.database import Base
from sqlalchemy.orm import relationship 
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    reports = relationship("Report", back_populates="user", cascade="all, delete")
    