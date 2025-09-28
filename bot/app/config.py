from pydantic import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    BACKEND_URL: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
