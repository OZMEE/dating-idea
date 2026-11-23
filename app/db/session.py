from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session

database_url = "sqlite:///./dating-ideas.db"
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
print(database_url)