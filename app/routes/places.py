from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import List, Place
from app.schemas import PlaceCreate, PlaceUpdate, PlaceResponse, ListResponse

router = APIRouter(prefix="/lists", tags=["places"])


# ① GET /lists/{list_id}/places
@router.get("/{list_id}/places", response_model=ListResponse)
def get_places(list_id: int, db: Session = Depends(get_db)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    return list_obj


# ② POST /lists/{list_id}/places（追加：重複防止）
@router.post("/{list_id}/places", response_model=PlaceResponse)
def create_place(list_id: int, place_data: PlaceCreate, db: Session = Depends(get_db)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")

    name = place_data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="掃除場所名を入力してください")

    # ✅ 重複チェック（同じリスト内）
    exists = db.query(Place).filter(
        Place.list_id == list_id,
        Place.name == name
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="同じ掃除場所名がすでに存在します"
        )

    new_place = Place(name=name, list_id=list_id)
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place


# ③ PUT /lists/places/{place_id}（編集：重複防止）
@router.put("/places/{place_id}", response_model=PlaceResponse)
def update_place(place_id: int, place_data: PlaceUpdate, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    name = place_data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="掃除場所名を入力してください")

    # ✅ 重複チェック（自分自身は除外）
    exists = db.query(Place).filter(
        Place.list_id == place.list_id,
        Place.name == name,
        Place.id != place_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="同じ掃除場所名がすでに存在します"
        )

    place.name = name
    db.commit()
    db.refresh(place)
    return place


# ④ DELETE /lists/places/{place_id}
@router.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    db.delete(place)
    db.commit()
    return {"message": "Place deleted"}
