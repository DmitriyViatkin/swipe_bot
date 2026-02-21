from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_BASE_URL: str
    # API_KEY: str=""
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


try:
    settings = Settings()
except Exception as e:
    print(f"Error configuration {e}")
    raise
