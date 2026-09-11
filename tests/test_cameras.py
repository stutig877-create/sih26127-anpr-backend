import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, Camera
from app.routes.cameras import create_camera, delete_camera, get_camera, list_cameras, update_camera
from app.schemas.camera import CameraCreate, CameraUpdate


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_camera_create_duplicate_get_update_delete(db):
    payload = CameraCreate(
        camera_id="CAM001",
        name="Main Gate",
        location="Sector 1",
        latitude=30.7333,
        longitude=76.7794,
    )
    created = create_camera(payload, db)
    assert created.camera_id == "CAM001"
    assert len(list_cameras(db)) == 1
    assert get_camera("CAM001", db).name == "Main Gate"

    with pytest.raises(HTTPException) as exc:
        create_camera(payload, db)
    assert exc.value.status_code == 409

    updated = update_camera("CAM001", CameraUpdate(status="inactive"), db)
    assert updated.status == "inactive"

    delete_camera("CAM001", db)
    with pytest.raises(HTTPException) as error:
        get_camera("CAM001", db)
    assert error.value.status_code == 404
