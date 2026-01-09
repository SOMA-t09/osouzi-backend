from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date
import re

# =========================
# List（部屋）
# =========================

class ListBase(BaseModel):
    title: str

    @field_validator("title")
    def title_not_blank(cls, v):
        if not v or not v.strip() or not v.replace("　", "").strip():
            raise ValueError("部屋名を入力してください。")
        return v


class ListCreate(ListBase):
    pass


class ListResponse(ListBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# =========================
# Place（掃除場所）
# =========================

class PlaceBase(BaseModel):
    name: str

    @field_validator("name")
    def name_not_blank(cls, v):
        if not v or not v.strip() or not v.replace("　", "").strip():
            raise ValueError("掃除場所名を入力してください。")
        return v


class PlaceCreate(PlaceBase):
    interval_days: int = Field(default=7, ge=1)


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    interval_days: Optional[int] = Field(default=None, ge=1)
    next_date: Optional[date] = None


class PlaceResponse(PlaceBase):
    id: int
    next_date: date
    interval_days: int

    class Config:
        from_attributes = True


# =========================
# List + Places（部屋一覧用）
# =========================

class ListWithPlacesResponse(BaseModel):
    id: int
    title: str
    places: List[PlaceResponse] = []

    class Config:
        from_attributes = True


# =========================
# User
# =========================

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("ユーザー名を入力してください")
        if not re.match(r"^[\u3040-\u309F_a-zA-Z0-9_-]+$", value):
            raise ValueError("使用できない文字が含まれています")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value.strip()) < 8:
            raise ValueError("パスワードは8文字以上です")
        return value


class UserLogin(BaseModel):
    username: str
    password: str

