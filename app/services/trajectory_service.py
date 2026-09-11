from sqlalchemy.orm import Session
from app.models.trajectory import Trajectory
from app.models.vehicle import Vehicle


class TrajectoryService:
    def __init__(self, db: Session):
        self.db = db

    def list_trajectories(self):
        return self.db.query(Trajectory).order_by(Trajectory.id).all()

    def get_trajectory(self, trajectory_id: int):
        return self.db.query(Trajectory).filter(Trajectory.id == trajectory_id).first()

    def get_vehicle_trajectory(self, plate_number: str):
        vehicle = self.db.query(Vehicle).filter(
            Vehicle.plate_number == plate_number
        ).first()
        if vehicle is None:
            return None

        points = self.db.query(Trajectory).filter(
            Trajectory.vehicle_id == vehicle.id
        ).order_by(Trajectory.sequence, Trajectory.timestamp, Trajectory.id).all()

        return {
            "plate_number": vehicle.plate_number,
            "vehicle_id": vehicle.id,
            "points": [
                {
                    "camera_id": point.camera_id,
                    "timestamp": point.timestamp,
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "sequence": point.sequence,
                }
                for point in points
            ],
        }

    def create_trajectory(self, vehicle_id: int, camera_id: str, timestamp, latitude: float, longitude: float, sequence: int = 1):
        trajectory = Trajectory(
            vehicle_id=vehicle_id,
            camera_id=camera_id,
            timestamp=timestamp,
            latitude=latitude,
            longitude=longitude,
            sequence=sequence,
        )
        self.db.add(trajectory)
        self.db.commit()
        self.db.refresh(trajectory)
        return trajectory

    def update_trajectory(self, trajectory: Trajectory, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(trajectory, field, value)
        self.db.commit()
        self.db.refresh(trajectory)
        return trajectory

    def delete_trajectory(self, trajectory: Trajectory):
        self.db.delete(trajectory)
        self.db.commit()
        return True
