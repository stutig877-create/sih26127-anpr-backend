from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.blacklist import BlacklistCreate, BlacklistUpdate, BlacklistResponse
from app.services.blacklist_service import BlacklistService

router = APIRouter(tags=["Blacklists"])


@router.post("/blacklist", response_model=BlacklistResponse, status_code=status.HTTP_201_CREATED)
@router.post("/blacklists", response_model=BlacklistResponse, status_code=status.HTTP_201_CREATED)
def create_blacklist(payload: BlacklistCreate, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    existing = service.get_blacklist_by_plate(payload.plate_number)
    if existing:
        raise HTTPException(status_code=400, detail="Blacklist plate already exists")

    return service.create_blacklist(
        plate_number=payload.plate_number,
        reason=payload.reason,
        created_by=payload.created_by,
    )


@router.get("/blacklist", response_model=list[BlacklistResponse])
@router.get("/blacklists", response_model=list[BlacklistResponse])
def list_blacklists(db: Session = Depends(get_db)):
    service = BlacklistService(db)
    return service.list_blacklists()


@router.get("/blacklist/{plate}", response_model=BlacklistResponse)
def get_blacklist_by_plate(plate: str, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    record = service.get_blacklist_by_plate(plate)
    if not record:
        raise HTTPException(status_code=404, detail="Blacklist record not found")
    return record


@router.delete("/blacklist/{plate}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklist_by_plate(plate: str, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    record = service.get_blacklist_by_plate(plate)
    if not record:
        raise HTTPException(status_code=404, detail="Blacklist record not found")
    service.delete_blacklist(record)


@router.get("/blacklists/{blacklist_id}", response_model=BlacklistResponse)
def get_blacklist(blacklist_id: int, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    record = service.get_blacklist(blacklist_id)
    if not record:
        raise HTTPException(status_code=404, detail="Blacklist record not found")
    return record


@router.put("/blacklists/{blacklist_id}", response_model=BlacklistResponse)
def update_blacklist(blacklist_id: int, payload: BlacklistUpdate, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    record = service.get_blacklist(blacklist_id)
    if not record:
        raise HTTPException(status_code=404, detail="Blacklist record not found")

    if payload.plate_number:
        duplicate = service.get_blacklist_by_plate(payload.plate_number)
        if duplicate and duplicate.id != blacklist_id:
            raise HTTPException(status_code=400, detail="Blacklist plate already exists")

    updated = service.update_blacklist(
        record,
        plate_number=payload.plate_number,
        reason=payload.reason,
        created_by=payload.created_by,
    )
    return updated


@router.delete("/blacklists/{blacklist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklist(blacklist_id: int, db: Session = Depends(get_db)):
    service = BlacklistService(db)
    record = service.get_blacklist(blacklist_id)
    if not record:
        raise HTTPException(status_code=404, detail="Blacklist record not found")

    service.delete_blacklist(record)
