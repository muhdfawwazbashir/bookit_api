from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.repositories import user as user_repo
from app.schemas.user import UserCreate, UserUpdate
from app.core import security, database
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def register_user(db: Session, user_data: UserCreate):
    # Check if email already exists
    existing_user = user_repo.get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Email already registered.")
    password_hash = get_password_hash(user_data.password)
    return user_repo.create_user(db, user_data, password_hash)

def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def update_user(db: Session, user_id: uuid.UUID, user_update: UserUpdate):
    password_hash = None
    if user_update.password:
        password_hash = get_password_hash(user_update.password)
    return user_repo.update_user(db, user_id, user_update, password_hash)

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    payload = security.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token.")
    user_id = payload.get("sub")
    user = user_repo.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user