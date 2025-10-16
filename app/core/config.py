from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    #db
    database_url: str = "postgresql://postgres:postgres@localhost:5432/emailschedulerdb"

    #security
    #scheduler_secret_key: str = "your-secret-key-here"

    # server
    port: int = 8000
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()