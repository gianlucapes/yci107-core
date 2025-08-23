from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    HF_TOKEN : str = os.getenv("HF_TOKEN")

settings = Settings()