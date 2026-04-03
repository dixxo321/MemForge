from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field(default="MemForge", env="MEMFORGE_APP_NAME")
    env: str = Field(default="development", env="MEMFORGE_ENV")
    debug: bool = Field(default=True, env="MEMFORGE_DEBUG")
    host: str = Field(default="127.0.0.1", env="MEMFORGE_HOST")
    port: int = Field(default=8000, env="MEMFORGE_PORT")

    database_url: str = Field(default="sqlite:///./memforge.db", env="MEMFORGE_DATABASE_URL")

    vector_backend: str = Field(default="simple", env="MEMFORGE_VECTOR_BACKEND")
    vector_dir: str = Field(default="./.memforge/vectors", env="MEMFORGE_VECTOR_DIR")

    embedding_provider: str = Field(default="dummy", env="MEMFORGE_EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="local-default", env="MEMFORGE_EMBEDDING_MODEL")

    log_level: str = Field(default="INFO", env="MEMFORGE_LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def vector_path(self) -> Path:
        return Path(self.vector_dir).resolve()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
