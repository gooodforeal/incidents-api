from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db"
    
    app_name: str = "Incidents API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

