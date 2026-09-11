from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertService:
    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(Alert).order_by(Alert.timestamp.desc(), Alert.id.desc())

    def list_alerts(self, active_only: bool = False):
        query = self._query()
        if active_only:
            query = query.filter(Alert.status == "active")
        return query.all()

    def get_alert(self, alert_id: int):
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def update_alert(self, alert: Alert, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(alert, field, value)
        self.db.commit()
        self.db.refresh(alert)
        return alert