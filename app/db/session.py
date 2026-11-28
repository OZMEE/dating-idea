from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session

from pathlib import Path

from app.models.base import Base

from app.models.auth import UserORM
from app.models.room import RoomORM
from app.models.participant import RoomParticipantORM
from app.models.option import OptionORM
from app.models.vote import VoteORM


BASE_DIR = Path(__file__).resolve().parent.parent.parent
database_url = f"sqlite:///{BASE_DIR / 'dating-ideas.db'}"
#todo: вернуть эту конфигурацию, чтобы подключиться к postgres
"""
settings = get_settings()

database_url = URL.create(
    drivername="postgresql",
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)
"""

# pool_pre_ping - нужен для проверки соединения
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker[Session](bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)
print(database_url)