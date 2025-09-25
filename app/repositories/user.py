from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
import uuid


def get_user_by_id(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate, password_hash: str):
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=password_hash,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: uuid.UUID, user_update: UserUpdate, password_hash: str = None):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    if user_update.name:
        db_user.name = user_update.name
    if password_hash:
        db_user.password_hash = password_hash

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: uuid.UUID):
    db_user = get_user_by_id(db, user_id)
    if not user_id:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
