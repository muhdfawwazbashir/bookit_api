from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import user as user_repo
from app.schemas.user import UserCreate
from app.core import security

def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user or not security.verify_password(password, user.password_hash):
        return None
    return user

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(token_data)
    return access_token, user


def refresh_access_token(refresh_token: str):
    payload = security.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return None
    user_id = payload.get("sub")
    access_token = security.create_access_token({"sub": user_id})
    return access_token