# config.py
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"  # Optional: load from .env file

settings = Settings()
