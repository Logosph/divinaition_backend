from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # LLM settings
    OPENROUTER_API_KEY: str = ""
    LLM_MODEL: str = "google/gemma-3-27b-it:free"
    LLM_API_URL: str = "https://openrouter.ai/api/v1/chat/completions"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 