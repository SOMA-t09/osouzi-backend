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


# ② POST /lists/{list_id}/places
@router.post("/{list_id}/places", response_model=PlaceResponse)
def create_place(list_id: int, place_data: PlaceCreate, db: Session = Depends(get_db)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")

    new_place = Place(name=place_data.name, list_id=list_id)
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place


# ③ PUT /lists/places/{place_id}  ← 追加
@router.put("/places/{place_id}", response_model=PlaceResponse)
def update_place(place_id: int, place_data: PlaceUpdate, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    place.name = place_data.name  # 名前を更新
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
