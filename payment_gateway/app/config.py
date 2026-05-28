from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mongodb://localhost:27017/payment_gateway"
    DATABASE_NAME: str = "payment_gateway"
    
    # Security
    SECRET_KEY: str = "your_super_secret_key_here_change_in_production"
    ENCRYPTION_KEY: str = "your_encryption_key_here_32_chars_for_aes256"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Payment Gateway"
    VERSION: str = "1.0.0"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Encryption
    ENCRYPT_SENSITIVE_DATA: bool = True
    ENCRYPTION_ALGORITHM: str = "AES"
    
    # Webhooks
    WEBHOOK_SECRET: str = "webhook_secret_key"
    WEBHOOK_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()