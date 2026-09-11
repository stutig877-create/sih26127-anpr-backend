from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Alert
from app.schemas.alert import AlertResponse, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter(tags=["Alerts"])


def serialize_alert(alert: Alert) -> dict:
    return {
        "id": alert.id,
        "vehicle": alert.vehicle_id,
        "plate": alert.plate_number,
        "camera": alert.camera_id,
        "timestamp": alert.timestamp,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "message": alert.message,
        "status": alert.status,
    }


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(db: Session = Depends(get_db)):
    return [serialize_alert(alert) for alert in AlertService(db).list_alerts()]


@router.get("/alerts/active", response_model=list[AlertResponse])
def list_active_alerts(db: Session = Depends(get_db)):
    return [serialize_alert(alert) for alert in AlertService(db).list_alerts(active_only=True)]


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = AlertService(db).get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return serialize_alert(alert)


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    service = AlertService(db)
    alert = service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    updated = service.update_alert(
        alert,
        status=payload.status,
        severity=payload.severity,
        message=payload.message,
    )
    return serialize_alert(updated)