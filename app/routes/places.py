from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models import List, Place
from app.schemas import (
    PlaceCreate,
    PlaceUpdate,
    PlaceResponse,
    ListResponse
)

router = APIRouter(prefix="/lists", tags=["places"])


# ------------------------------
# GET /lists/{list_id}/places
# ------------------------------
from app.schemas import ListWithPlacesResponse

@router.get("/{list_id}/places", response_model=ListWithPlacesResponse)
def get_places(list_id: int, db: Session = Depends(get_db)):
    list_obj = (
        db.query(List)
        .options(joinedload(List.places))
        .filter(List.id == list_id)
        .first()
    )

    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")

    return list_obj


# ------------------------------
# POST /lists/{list_id}/places
# ------------------------------
@router.post("/{list_id}/places", response_model=PlaceResponse)
def create_place(list_id: int, place_data: PlaceCreate, db: Session = Depends(get_db)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")

    name = place_data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="掃除場所名を入力してください")

    # 重複チェック
    exists = db.query(Place).filter(
        Place.list_id == list_id,
        Place.name == name
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="同じ掃除場所名が存在します")

    new_place = Place(
        name=name,
        list_id=list_id,
        interval_days=place_data.interval_days,
        next_date=date.today()
    )

    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place


# ------------------------------
# PUT /lists/places/{place_id}
# （編集 & 完了）
# ------------------------------
@router.put("/places/{place_id}", response_model=PlaceResponse)
def update_place(place_id: int, place_data: PlaceUpdate, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # 名前変更
    if place_data.name is not None:
        name = place_data.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="掃除場所名を入力してください")

        exists = db.query(Place).filter(
            Place.list_id == place.list_id,
            Place.name == name,
            Place.id != place_id
        ).first()

        if exists:
            raise HTTPException(status_code=400, detail="同じ掃除場所名が存在します")

        place.name = name

    # 期間変更
    if place_data.interval_days is not None:
        place.interval_days = place_data.interval_days

    # 完了 or 手動日付変更
    if place_data.next_date is not None:
        place.next_date = place_data.next_date

    db.commit()
    db.refresh(place)
    return place


# ------------------------------
# DELETE /lists/places/{place_id}
# ------------------------------
@router.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    db.delete(place)
    db.commit()
    return {"message": "Place deleted"}
