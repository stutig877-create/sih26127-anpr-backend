from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Camera
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate
from app.services.camera_service import CameraService

router = APIRouter(tags=["Cameras"])


@router.post("/cameras", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(payload: CameraCreate, db: Session = Depends(get_db)):
    service = CameraService(db)
    existing = service.get_camera(payload.camera_id)
    if existing:
        raise HTTPException(status_code=409, detail="Camera already exists")

    if payload.status not in {"active", "inactive", "offline"}:
        raise HTTPException(status_code=400, detail="Invalid camera status")

    if payload.latitude < -90 or payload.latitude > 90:
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

    if payload.longitude < -180 or payload.longitude > 180:
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    camera = service.create_camera(
        camera_id=payload.camera_id,
        name=payload.name,
        location=payload.location,
        latitude=payload.latitude,
        longitude=payload.longitude,
        status=payload.status,
    )
    return camera


@router.get("/cameras", response_model=list[CameraResponse])
def list_cameras(db: Session = Depends(get_db)):
    service = CameraService(db)
    return service.list_cameras()


@router.get("/cameras/{camera_id}", response_model=CameraResponse)
def get_camera(camera_id: str, db: Session = Depends(get_db)):
    service = CameraService(db)
    camera = service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera


@router.put("/cameras/{camera_id}", response_model=CameraResponse)
def update_camera(camera_id: str, payload: CameraUpdate, db: Session = Depends(get_db)):
    service = CameraService(db)
    camera = service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    if payload.status and payload.status not in {"active", "inactive", "offline"}:
        raise HTTPException(status_code=400, detail="Invalid camera status")

    if payload.latitude is not None and (payload.latitude < -90 or payload.latitude > 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

    if payload.longitude is not None and (payload.longitude < -180 or payload.longitude > 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    updated = service.update_camera(
        camera,
        name=payload.name,
        location=payload.location,
        latitude=payload.latitude,
        longitude=payload.longitude,
        status=payload.status,
    )
    return updated


@router.delete("/cameras/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(camera_id: str, db: Session = Depends(get_db)):
    service = CameraService(db)
    camera = service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    service.delete_camera(camera)
