from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db
from app.models.auth import User
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, UserResponse

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@auth_router.post("/register", status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    raise NotImplementedError


@auth_router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    raise NotImplementedError


@auth_router.post("/refresh")
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    raise NotImplementedError

@auth_router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    raise NotImplementedError