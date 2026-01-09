# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    lists = relationship(
        "List",
        back_populates="user",
        cascade="all, delete"
    )


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="lists")

    # 掃除場所
    places = relationship(
        "Place",
        back_populates="list",
        cascade="all, delete"
    )


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    list = relationship("List", back_populates="places")

    # 次回掃除日（完了ボタンで更新）
    next_date = Column(
        Date,
        nullable=False,
        default=date.today
    )

    # 掃除間隔（日）
    interval_days = Column(
        Integer,
        nullable=False,
        default=7
    )
