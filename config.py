import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

class Config:
    SENSOR_ID: str = os.getenv("SENSOR_ID", "civwatch-sensor-01")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./civwatch.db")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SCORER_VERSION: str = "3.0.1"
    BASELINE_VERSION: str = "3.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkeyforcivwatch")

config = Config()