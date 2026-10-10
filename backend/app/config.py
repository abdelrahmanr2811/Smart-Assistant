import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Smart Assistant - Construction PM AI"
    APP_ENV: str = "development"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"

    # Security & JWT Tokens
    JWT_SECRET_KEY: str = "smart-assistant-construction-pm-super-secret-key-2026-secure"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ALLOWED_ORIGINS: List[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://localhost:3000"
    ]

    # LLM Settings
    LLM_PROVIDER: str = "gemini"  # "gemini", "openai", "local"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.5-flash"

    # Whisper Settings
    WHISPER_MODE: str = "local_whisper"  # "openai_cloud" or "local_whisper"
    WHISPER_LOCAL_MODEL: str = "base"

    # Storage Paths & Chroma Telemetry
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'data' / 'smart_assistant.db'}"
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "data" / "chromadb")
    CHROMA_TELEMETRY_ENABLED: bool = False
    UPLOAD_DIR: str = str(BASE_DIR / "data" / "uploads")

    # Email Settings (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "smart.pm.assistant@company.com"
    SMTP_USE_TLS: bool = True

    # Calendar Integration (ICS & Optional API credentials)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="allow"
    )

settings = Settings()

# Enforce strong secret in production
if settings.APP_ENV == "production":
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY in ["secret", "password", "default", "123456"]:
        raise ValueError("FATAL SECURITY ERROR: Production deployment requires setting a strong JWT_SECRET_KEY in environment variables.")

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs(BASE_DIR / "data", exist_ok=True)
