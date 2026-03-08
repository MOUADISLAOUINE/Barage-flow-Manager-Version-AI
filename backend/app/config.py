from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Barrage-Flow Manager"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://bfm_user:bfm_pass@db:5432/barrage_flow"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Security
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # MFA
    MFA_ISSUER: str = "BarrageFlowManager"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # -------------------------------------------------------
    # Dam Business Rules — configurable, NEVER hard-coded
    # These are defaults; live values are stored in the DB
    # and loaded at runtime by the dam service.
    # -------------------------------------------------------
    DEFAULT_SAFETY_RESERVE_PCT: float = 25.0   # Critical zone threshold
    DEFAULT_WARNING_ZONE_PCT: float = 40.0     # Warning zone threshold
    DEFAULT_ALERT_ZONE_PCT: float = 60.0       # Alert zone threshold

    # Priority weights for the Fair Share Formula
    PRIORITY_WEIGHT_CLASS_A: float = 1.5
    PRIORITY_WEIGHT_CLASS_B: float = 1.0
    PRIORITY_WEIGHT_CLASS_C: float = 0.6

    # Alert zone allocation reduction factors
    ALERT_ZONE_REDUCTION: float = 0.10    # 10% reduction in Alert zone
    WARNING_ZONE_REDUCTION: float = 0.30  # 30% reduction in Warning zone

    # Email alerts
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    ALERT_RECIPIENTS: List[str] = []

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
