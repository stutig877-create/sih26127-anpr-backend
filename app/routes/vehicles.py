from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleHistoryResponse, VehicleResponse, VehicleUpdate
from app.services.vehicle_service import VehicleService

router = APIRouter(tags=["Vehicles"])


@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    service = VehicleService(db)
    existing = service.get_vehicle_by_plate(payload.plate_number)
    if existing:
        raise HTTPException(status_code=400, detail="Vehicle already exists")

    vehicle = service.create_vehicle(
        plate_number=payload.plate_number,
        camera_id=payload.camera_id,
        timestamp=payload.timestamp,
        location=payload.location,
    )
    return vehicle


@router.get("/vehicles", response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db)):
    service = VehicleService(db)
    return service.list_vehicles()


@router.get("/vehicles/{plate_number}/history", response_model=list[VehicleHistoryResponse])
def get_vehicle_history(plate_number: str, db: Session = Depends(get_db)):
    service = VehicleService(db)
    history = service.get_history_by_plate(plate_number.strip().upper())
    if history is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return history


@router.get("/vehicle/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    service = VehicleService(db)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.get("/vehicles/{plate_number}", response_model=VehicleResponse)
def get_vehicle(plate_number: str, db: Session = Depends(get_db)):
    service = VehicleService(db)
    vehicle = service.get_vehicle_by_plate(plate_number.strip().upper())
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    service = VehicleService(db)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    updated = service.update_vehicle(
        vehicle,
        plate_number=payload.plate_number,
        camera_id=payload.camera_id,
        timestamp=payload.timestamp,
        location=payload.location,
    )
    return updated


@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    service = VehicleService(db)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    service.delete_vehicle(vehicle)
