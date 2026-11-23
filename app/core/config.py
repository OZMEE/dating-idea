import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

def get_settings() -> Settings:
    return Settings(
        DB_PORT=os.environ.get("DB_PORT", 5432),
        DB_HOST=os.environ.get("DB_HOST", "db"),
        DB_USERNAME=os.environ.get("DB_USERNAME", "user"),
        DB_PASSWORD=os.environ.get("DB_PASSWORD", "password"),
        DB_NAME=os.environ.get("DB_NAME", "dating-ideas"),
    )