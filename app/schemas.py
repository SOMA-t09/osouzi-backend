from pydantic import BaseModel,Field,field_validator
from typing import Optional
from datetime import datetime
import re

# 基本のタスクスキーマ
class TodoBase(BaseModel):
    title: str  # タスクのタイトル（必須）
    details: Optional[str] = None  # タスクの詳細（任意）

# タスク作成用のスキーマ
class TodoCreate(TodoBase):
    pass  # TodoBaseと同じ内容なので、そのまま継承

# タスクレスポンス用のスキーマ
class TodoResponse(TodoBase):
    id: int  # タスクID
    createdAt: datetime  # 作成日時
    updatedAt: datetime  # 更新日時
    completed: bool  # 完了フラグ

    class Config:
        # ORM（データベースモデル）からデータを読み取る設定
        from_attributes = True

from pydantic import BaseModel

# ユーザー登録用のスキーマ
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3,  description="ユーザー名（ひらがな・英数字・_・-）")
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")

    @field_validator("username")
    def validate_username(cls, value):
        # 空白・スペースのみ禁止
        if not value.strip():
            raise ValueError("ユーザー名を入力してください。（空白のみは不可）")

        # ひらがな＋英数字＋_・- のみ許可
        if not re.match(r"^[\u3040-\u309F_a-zA-Z0-9-]+$", value.strip()):
            raise ValueError("ユーザー名はひらがな・英数字・_・-のみ使用できます。")

        return value.strip()

    @field_validator("password")
    def validate_password(cls, value):
        # 空白・スペースのみ禁止
        if not value.strip():
            raise ValueError("パスワードを入力してください。（空白のみは不可）")

        # 英字・数字・記号をすべて含むかチェック
        password = value.strip()
        has_letter = re.search(r"[A-Za-z]", password)
        has_number = re.search(r"[0-9]", password)
        has_symbol = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if not (has_letter and has_number and has_symbol):
            raise ValueError("パスワードは英字・数字・記号をそれぞれ1文字以上含めてください。")

        return password

    class Config:
        from_attributes = True

# ユーザーログイン用のスキーマ
class UserLogin(BaseModel):
    username: str  # ユーザー名
    password: str  # パスワード

    class Config:
        from_attributes = True