from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user
from app.services.auth_service import AuthService

router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", summary="Register a new customer account")
def register(body: RegisterRequest, db=Depends(get_db)):
    try:
        return AuthService(db).register(
            name=body.name,
            email=body.email,
            password=body.password,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", summary="Login and receive a JWT token")
def login(body: LoginRequest, db=Depends(get_db)):
    try:
        return AuthService(db).login(email=body.email, password=body.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", summary="Get current user profile")
def me(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    try:
        return AuthService(db).get_me(current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))