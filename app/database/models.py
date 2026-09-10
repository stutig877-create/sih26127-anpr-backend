from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(50), unique=True, index=True, nullable=False)
    camera_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String(255), nullable=True)


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    image_path = Column(String(255), nullable=False)
    confidence = Column(Float, default=0.0)

    vehicle = relationship("Vehicle")


class UploadFileRecord(Base):
    __tablename__ = "upload_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
