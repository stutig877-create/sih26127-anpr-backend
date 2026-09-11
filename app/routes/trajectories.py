from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.trajectory import (
    TrajectoryCreate,
    TrajectoryUpdate,
    TrajectoryResponse,
    VehicleTrajectoryResponse,
)
from app.services.trajectory_service import TrajectoryService

router = APIRouter(tags=["Trajectories"])


@router.get("/vehicles/{plate_number}/trajectory", response_model=VehicleTrajectoryResponse)
def get_vehicle_trajectory(plate_number: str, db: Session = Depends(get_db)):
    service = TrajectoryService(db)
    trajectory = service.get_vehicle_trajectory(plate_number.strip().upper())
    if trajectory is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return trajectory


@router.post("/trajectories", response_model=TrajectoryResponse, status_code=status.HTTP_201_CREATED)
def create_trajectory(payload: TrajectoryCreate, db: Session = Depends(get_db)):
    service = TrajectoryService(db)

    if payload.latitude < -90 or payload.latitude > 90:
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

    if payload.longitude < -180 or payload.longitude > 180:
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    trajectory = service.create_trajectory(
        vehicle_id=payload.vehicle_id,
        camera_id=payload.camera_id,
        timestamp=payload.timestamp,
        latitude=payload.latitude,
        longitude=payload.longitude,
        sequence=payload.sequence,
    )
    return trajectory


@router.get("/trajectories", response_model=list[TrajectoryResponse])
def list_trajectories(db: Session = Depends(get_db)):
    service = TrajectoryService(db)
    return service.list_trajectories()


@router.get("/trajectories/{trajectory_id}", response_model=TrajectoryResponse)
def get_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    service = TrajectoryService(db)
    trajectory = service.get_trajectory(trajectory_id)
    if not trajectory:
        raise HTTPException(status_code=404, detail="Trajectory not found")
    return trajectory


@router.put("/trajectories/{trajectory_id}", response_model=TrajectoryResponse)
def update_trajectory(trajectory_id: int, payload: TrajectoryUpdate, db: Session = Depends(get_db)):
    service = TrajectoryService(db)
    trajectory = service.get_trajectory(trajectory_id)
    if not trajectory:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    if payload.latitude is not None and (payload.latitude < -90 or payload.latitude > 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

    if payload.longitude is not None and (payload.longitude < -180 or payload.longitude > 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    updated = service.update_trajectory(
        trajectory,
        vehicle_id=payload.vehicle_id,
        camera_id=payload.camera_id,
        timestamp=payload.timestamp,
        latitude=payload.latitude,
        longitude=payload.longitude,
        sequence=payload.sequence,
    )
    return updated


@router.delete("/trajectories/{trajectory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    service = TrajectoryService(db)
    trajectory = service.get_trajectory(trajectory_id)
    if not trajectory:
        raise HTTPException(status_code=404, detail="Trajectory not found")

    service.delete_trajectory(trajectory)
