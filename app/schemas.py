from pydantic import BaseModel,Field,field_validator
from typing import Optional
from datetime import datetime
import re

class ListBase(BaseModel):
    title: str

    @field_validator("title")
    def title_not_blank(cls, v):
        # 半角・全角スペースのみを禁止
        if not v or not v.strip() or not v.replace("　", "").strip():
            raise ValueError("部屋名を入力してください。")
        return v

class ListCreate(ListBase):
    pass

class ListResponse(ListBase):
    id: int
    title:str
    user_id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str = Field(..., description="ユーザー名（ひらがな・英数字・_・-）")
    password: str = Field(..., description="パスワード（8文字以上）")

    @field_validator("username")
    def validate_username(cls, value):
        # 前後スペース削除
        clean_value = value.strip()

        # 空白のみ禁止
        if not clean_value:
            raise ValueError("ユーザー名を入力してください。（空白のみは不可）")

        # スペースを除いた文字数で判定
        if len(re.sub(r"\s", "", clean_value)) < 3:
            raise ValueError("ユーザー名は3文字以上で入力してください。（スペースは含まれません）")

        # 使用可能文字チェック
        if not re.match(r"^[\u3040-\u309F_a-zA-Z0-9-]+$", clean_value.replace(" ", "")):
            raise ValueError("ユーザー名はひらがな・英数字・_・-のみ使用できます。")

        return clean_value

    @field_validator("password")
    def validate_password(cls, value):
        clean_value = value.strip()

        # 空白のみ禁止
        if not clean_value:
            raise ValueError("パスワードを入力してください。（空白のみは不可）")

        # スペース除外して長さ確認
        if len(re.sub(r"\s", "", clean_value)) < 8:
            raise ValueError("パスワードは8文字以上で入力してください。（スペースは含まれません）")

        # 英字・数字・記号を含むか確認
        password = re.sub(r"\s", "", clean_value)
        has_letter = re.search(r"[A-Za-z]", password)
        has_number = re.search(r"[0-9]", password)
        has_symbol = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if not (has_letter and has_number and has_symbol):
            raise ValueError("パスワードは英字・数字・記号をそれぞれ1文字以上含めてください。")

        return clean_value
    
    class Config:
        from_attributes = True

# ユーザーログイン用のスキーマ
class UserLogin(BaseModel):
    username: str  # ユーザー名
    password: str  # パスワード

    class Config:
        from_attributes = True


# app/schemas.py
from pydantic import BaseModel

class PlaceBase(BaseModel):
    name: str

class PlaceCreate(PlaceBase):
    pass

class PlaceResponse(PlaceBase):
    id: int

    class Config:
        from_attributes = True

class ListResponse(BaseModel):
    id: int
    title: str
    places: list[PlaceResponse]

    class Config:
        from_attributes = True
