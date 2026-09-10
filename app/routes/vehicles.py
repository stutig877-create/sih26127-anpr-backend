from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse
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


@router.get("/vehicle/{vehicle_id}", response_model=VehicleResponse)
@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
