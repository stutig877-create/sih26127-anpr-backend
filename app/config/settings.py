from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sih26127.db"
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UPLOAD_DIR: str = "uploads"
    ALLOWED_IMAGE_TYPES: tuple[str, ...] = ("image/jpeg", "image/png", "image/jpg")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
