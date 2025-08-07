# carte ur routs user_router.py
from fastapi import APIRouter, Depends, HTTPException
from utils.helpers import has_exception
from sqlalchemy.orm import Session
from db.session import get_db
from crud.user_crud import (
    create_user,
    get_user,
    update_user,
    delete_user,
    get_all_users,
    admin_approve_user,
    get_all_active_users,
    get_all_admin_approved_users,
)
from schemas.user import UserCreate, UserUpdate, UserOut, UserWithTokens, LoginRequest, ResponseModel
from models.user import User
from models.token import Token
from services.token_services import create_access_token, create_refresh_token 
from services.token_services import decode_jwt_token  # your JWT decoding logic
from fastapi.security import OAuth2PasswordBearer

# Create a new APIRouter instance
router = APIRouter()

# Dependency to get the database session
def get_db_session(db: Session = Depends(get_db)):
    return db

# Create a new user
@router.post("/register", response_model=ResponseModel)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db_session)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    user_data = create_user(db, user)
    
    if not user_data:
        raise HTTPException(status_code=500, detail="User creation failed")
    
    return {
        "data": user_data,
        "message": "User created successfully, please wait for admin approval",
        "status": "success"
    }
        

@router.post("/login", response_model=UserWithTokens)
def login_user(login: LoginRequest, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == login.username).first()
    if not user or not user.verify_password(login.password):
        raise HTTPException(status_code=404, detail="User not found")
    
    # if user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin users cannot log in through this endpoint")
    
    print(f"User found: {user}")

    if not user.is_admin_approved:
        raise HTTPException(status_code=403, detail="User not approved by admin")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    # Create Token instance and store in DB
    token_obj = Token(user_id=user.id, access_token=access_token, refresh_token=refresh_token)
    db.add(token_obj)
    db.commit()
    db.refresh(user)

    return {
        "data": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Login successful",
        "status": "success"
    }



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)) -> User:
    payload = decode_jwt_token(token)
    print(f"Decoded payload: {payload}")
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:  # assuming `is_admin` is a Boolean column in User model
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# approved user by admin
@router.post("/{user_id}/approve", response_model=UserOut)
def approve_user(user_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(admin_required)):
    user = admin_approve_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

