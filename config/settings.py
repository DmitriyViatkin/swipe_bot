from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from functools import lru_cache

from pydantic import Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class BaseInfraSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class BotSettings(BaseInfraSettings):
    BOT_TOKEN: str
    API_BASE_URL: str

    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class RedisSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
    )

    HOST: str = "redis"
    PORT: int = 6379
    PASSWORD: Optional[str] = None
    DB: int = 0

    @property
    def url(self) -> str:
        if self.PASSWORD:
            return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


class InfraSettings(BaseInfraSettings):
    bot: BotSettings = Field(default_factory=BotSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)


# --- GLOBAL CONFIG SINGLETON ---
@lru_cache
def get_infra_settings() -> InfraSettings:
    """Единственная функция для получения кэшированных настроек."""
    return InfraSettings()


# --- ЭКСПОРТ ГОТОВЫХ К ИСПОЛЬЗОВАНИЮ ОБЪЕКТОВ ---


infra_settings = get_infra_settings()


redis_settings = infra_settings.redis
