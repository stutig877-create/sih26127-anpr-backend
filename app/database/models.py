from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="operator")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detections = relationship("Detection", back_populates="camera")
    trajectories = relationship("Trajectory", back_populates="camera")
    alerts = relationship("Alert", back_populates="camera")
    vehicles = relationship("Vehicle", back_populates="camera")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(50), unique=True, index=True, nullable=False)
    camera_id = Column(String(50), ForeignKey("cameras.camera_id"), nullable=False)
    vehicle_type = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    location = Column(String(255), nullable=True)
    confidence = Column(Float, default=0.0)

    camera = relationship("Camera", back_populates="vehicles")
    detections = relationship("Detection", back_populates="vehicle")
    trajectories = relationship("Trajectory", back_populates="vehicle")
    alerts = relationship("Alert", back_populates="vehicle")


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    camera_id = Column(String(50), ForeignKey("cameras.camera_id"), nullable=False)
    plate_number = Column(String(50), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, default=0.0)
    vehicle_type = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    image_path = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="detections")
    camera = relationship("Camera", back_populates="detections")
    alerts = relationship("Alert", back_populates="detection")


class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    camera_id = Column(String(50), ForeignKey("cameras.camera_id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sequence = Column(Integer, nullable=False, default=1)

    vehicle = relationship("Vehicle", back_populates="trajectories")
    camera = relationship("Camera", back_populates="trajectories")


class Blacklist(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(50), unique=True, index=True, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(255), nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    plate_number = Column(String(50), index=True, nullable=False)
    camera_id = Column(String(50), ForeignKey("cameras.camera_id"), nullable=False)
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String(50), nullable=False, default="blacklist")
    severity = Column(String(50), nullable=False, default="high")
    message = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="active")

    vehicle = relationship("Vehicle", back_populates="alerts")
    camera = relationship("Camera", back_populates="alerts")
    detection = relationship("Detection", back_populates="alerts")


class UploadFileRecord(Base):
    __tablename__ = "upload_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
