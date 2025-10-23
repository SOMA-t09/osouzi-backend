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