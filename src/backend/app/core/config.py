from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = ""

    # Security
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"

    # Bot
    BOT_TOKEN: str = ""
    BACKEND_URL: str = ""

    # Любые дополнительные настройки можно добавить сюда
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# Создаём единственный объект настроек для всего проекта
settings = Settings()
