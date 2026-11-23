import os

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.auth import User

security = HTTPBearer(auto_error=False)

DEV_MODE = os.getenv("ENV") == "development"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if DEV_MODE:
        user = User()
        user.name = "dev_user"
        print(user)
        return user
    raise NotImplementedError
