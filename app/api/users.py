from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user as user_service
from app.core.database import get_db
from typing import List
import uuid


router = APIRouter(tags=["Users"])


@router.get(" {current user profile}", response_model=UserOut)
def get_me(current_user=Depends(user_service.get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching user profile failed: {str(e)}")


@router.patch("", response_model=UserOut)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(user_service.get_current_user)
):
    try:
        updated_user = user_service.update_user(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Update failed: User not found")
        return updated_user
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")