from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import List, User
from app.schemas import ListCreate, ListResponse
from app.database import get_db
from app.routes.auth import get_current_user

router = APIRouter(prefix="/lists", tags=["lists"])

@router.post("/", response_model=ListResponse)
def create_list(
    list_data: ListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("🟢 create_list called", list_data, current_user.id)

    # ✅ 重複チェック（同じユーザー & 同じタイトル）
    existing = db.query(List).filter(
        List.user_id == current_user.id,
        List.title == list_data.title
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="同じ部屋名はすでに存在します")

    try:
        new_list = List(title=list_data.title, user_id=current_user.id)
        db.add(new_list)
        db.commit()
        db.refresh(new_list)
        print("✅ List inserted:", new_list.id, new_list.title)
        return new_list
    except Exception as e:
        db.rollback()
        print("❌ DBエラー:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    list_item = db.query(List).filter(List.id == list_id, List.user_id == current_user.id).first()
    if not list_item:
        raise HTTPException(status_code=404, detail="リストが見つかりません")
    db.delete(list_item)
    db.commit()
    return {"message": "削除しました"}


@router.put("/{list_id}", response_model=ListResponse)
def update_list(
    list_id: int,
    list_data: ListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    list_item = db.query(List).filter(List.id == list_id, List.user_id == current_user.id).first()
    if not list_item:
        raise HTTPException(status_code=404, detail="リストが見つかりません")

    # ✅ 他のリストと重複するタイトルがないか確認
    existing = db.query(List).filter(
        List.user_id == current_user.id,
        List.title == list_data.title,
        List.id != list_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="同じ部屋名はすでに存在します")

    list_item.title = list_data.title
    db.commit()
    db.refresh(list_item)
    return list_item


@router.get("/", response_model=list[ListResponse])
def get_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lists = db.query(List).filter(List.user_id == current_user.id).all()
    return lists
