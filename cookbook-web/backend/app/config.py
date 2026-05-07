from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    LLM_FORMAT: Literal["openai", "anthropic"] = "openai"
    LLM_ENDPOINT: str = "http://localhost:11434/v1"
    LLM_API_KEY: str = "no-key"
    LLM_MODEL: str = "llama3"
    LLM_TIMEOUT_SECONDS: int = 120

    COOKBOOK_DIR: Path = Path("/app/cookbooks")
    DATA_DIR: Path = Path("/data")
    FRONTEND_DIST: Path = Path("/app/frontend/dist")

    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-small"
    EMBEDDING_CACHE: Path = Path("/app/models")
    RAG_TOP_K: int = 5
    RAG_MAX_PAGE_CHARS: int = 2000


settings = Settings()
