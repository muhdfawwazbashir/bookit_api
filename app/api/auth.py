from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, TokenResponse, LoginRequest
from app.services import auth as auth_service 
from app.services import user as user_service
from app.core.database import get_db



router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    
@router.post("/login", response_model=TokenResponse)
def login(login_data:LoginRequest, db: Session = Depends(get_db)):
    user_email = login_data.email
    password = login_data.password
        
    token, user = auth_service.login_user(db, user_email, password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials.")
    
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh")
def refresh():
    return {"message": "Refresh logic not implemented."}

@router.post("/logout")
def logout():
    return {"message": "Logout from Swagger Authorize."}
