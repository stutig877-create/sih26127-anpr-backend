from sqlalchemy.orm import Session
from app.models.camera import Camera


class CameraService:
    def __init__(self, db: Session):
        self.db = db

    def list_cameras(self):
        return self.db.query(Camera).order_by(Camera.id).all()

    def get_camera(self, camera_id: str):
        return self.db.query(Camera).filter(Camera.camera_id == camera_id).first()

    def create_camera(self, camera_id: str, name: str, location: str, latitude: float, longitude: float, status: str):
        camera = Camera(
            camera_id=camera_id,
            name=name,
            location=location,
            latitude=latitude,
            longitude=longitude,
            status=status,
        )
        self.db.add(camera)
        self.db.commit()
        self.db.refresh(camera)
        return camera

    def update_camera(self, camera: Camera, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(camera, field, value)
        self.db.commit()
        self.db.refresh(camera)
        return camera

    def delete_camera(self, camera: Camera):
        self.db.delete(camera)
        self.db.commit()
        return True
