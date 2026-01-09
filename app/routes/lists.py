from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import List, User
from app.schemas import (
    ListCreate,
    ListResponse,
    ListWithPlacesResponse,
)
from app.routes.auth import get_current_user

router = APIRouter(prefix="/lists", tags=["lists"])


# =========================
# 作成
# =========================

@router.post("/", response_model=ListResponse)
def create_list(
    list_data: ListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(List)
        .filter(
            List.user_id == current_user.id,
            List.title == list_data.title,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="同じ部屋名はすでに存在します")

    new_list = List(
        title=list_data.title,
        user_id=current_user.id,
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list


# =========================
# 一覧取得（🔥 ここが最重要）
# =========================

@router.get("/", response_model=list[ListWithPlacesResponse])
def get_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lists = (
        db.query(List)
        .filter(List.user_id == current_user.id)
        .all()
    )
    return lists


# =========================
# 更新
# =========================

@router.put("/{list_id}", response_model=ListResponse)
def update_list(
    list_id: int,
    list_data: ListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    list_item = (
        db.query(List)
        .filter(
            List.id == list_id,
            List.user_id == current_user.id,
        )
        .first()
    )

    if not list_item:
        raise HTTPException(status_code=404, detail="リストが見つかりません")

    existing = (
        db.query(List)
        .filter(
            List.user_id == current_user.id,
            List.title == list_data.title,
            List.id != list_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="同じ部屋名はすでに存在します")

    list_item.title = list_data.title
    db.commit()
    db.refresh(list_item)
    return list_item


# =========================
# 削除
# =========================

@router.delete("/{list_id}")
def delete_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    list_item = (
        db.query(List)
        .filter(
            List.id == list_id,
            List.user_id == current_user.id,
        )
        .first()
    )

    if not list_item:
        raise HTTPException(status_code=404, detail="リストが見つかりません")

    db.delete(list_item)
    db.commit()
    return {"message": "削除しました"}
