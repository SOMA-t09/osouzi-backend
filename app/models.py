from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    lists = relationship("List", back_populates="user")

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Userとのリレーション
    user = relationship("User", back_populates="lists")

