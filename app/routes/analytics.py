from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["Analytics"])


@router.get("/analytics", summary="Return dashboard analytics", description="Return simple analytics counts from detections and vehicles.")
def get_analytics(db: Session = Depends(get_db)):
    return AnalyticsService(db).vehicle_count()


@router.get("/analytics/vehicle-count")
def get_vehicle_count(db: Session = Depends(get_db)):
    return AnalyticsService(db).vehicle_count()


@router.get("/analytics/camera-traffic")
def get_camera_traffic(db: Session = Depends(get_db)):
    return {"cameras": AnalyticsService(db).camera_traffic()}


@router.get("/analytics/congestion")
def get_congestion(db: Session = Depends(get_db)):
    return AnalyticsService(db).congestion()


@router.get("/analytics/origin-destination")
def get_origin_destination(db: Session = Depends(get_db)):
    return {"routes": AnalyticsService(db).origin_destination()}
