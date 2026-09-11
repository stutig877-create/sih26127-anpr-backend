import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, User
from app.routes.auth import login, register
from app.schemas.auth import LoginRequest, RegisterRequest


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


def test_register_and_login(db):
    user = register(
        RegisterRequest(
            email="operator@example.com",
            password="StrongPass123",
            full_name="Test Operator",
            role="operator",
        ),
        db,
    )
    stored = db.query(User).filter(User.id == user.id).one()
    assert stored.password_hash != "StrongPass123"

    token = login(LoginRequest(email="operator@example.com", password="StrongPass123"), db)
    assert token["token_type"] == "bearer"
    assert token["user"].role == "operator"


def test_invalid_login(db):
    register(
        RegisterRequest(
            email="operator@example.com",
            password="StrongPass123",
            full_name="Test Operator",
            role="operator",
        ),
        db,
    )

    with pytest.raises(HTTPException) as exc:
        login(LoginRequest(email="operator@example.com", password="WrongPass123"), db)
    assert exc.value.status_code == 401
