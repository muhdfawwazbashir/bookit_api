from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.services import auth as auth_service 
from app.services import user as user_service
from app.core.database import get_db


router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    
@router.post("/login")
def login(form_data:dict, db: Session = Depends(get_db)):
    email = form_data.get("email")
    password = form_data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")
    token, user = auth_service.login_user(db, email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials.")
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/refresh")
def refresh():
    return {"message": "Refresh logic not implemented."}

@router.post("/logout")
def logout():
    return {"message": "Logout logic will go here."}



# @router.post("/resgister", response_model=UserOut)
# def register(user: UserCreate):
#     return register_user(user)


# @router.post("/login")
# def login(email: str, password: str):
#     return login_user(email, password)

# @router.post("/refresh")
# def refresh():
#     return


# @router.post("/logout")
# def logout():
#     return


# @router.post("/register", response_model=user.UserCreate)
# def register(user_data: user.UserCreate, db: Session = Depends(get_db)):
#     """Register a new user and send OTP email"""
#     try:
#         # Check if user already exists
#         existing_user = db.query(User).filter(User.email == user_data.email).first()
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Email already registered")
        
#         # db_user = User(
#         #     id = User.id,
#         #     email = user_data.email,
#         #     # password_hash = password_hash,

#         # )
#     except HTTPException:
#         db.rollback()
#         raise
#     except Exception as e:
#         db.rollback()
#         print(f"Registration error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

