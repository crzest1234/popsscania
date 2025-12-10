from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from .db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source_url = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    metadata = Column(JSON, default={})
    ml_result = Column(JSON, default={})
    estimated_works = Column(JSON, default={})
    rentability = Column(JSON, default={})
    pdf_path = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")
