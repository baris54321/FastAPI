# carte ur routs user_router.py
from fastapi import APIRouter, Depends, HTTPException
from utils.helpers import has_exception
from sqlalchemy.orm import Session
from db.session import get_db_session
from crud.user_crud import (
    create_user,
    get_all_users,
    get_unapproved_users,
    get_all_admin_approved_users,
)
from schemas.user import UserCreate, UserOut, UserWithTokens, LoginRequest, ResponseModel, ApproveUser
from models.user import User
from models.token import Token
from services.token_services import create_access_token, create_refresh_token, get_current_user 

# Create a new APIRouter instance
router = APIRouter()

# Create a new user
@router.post("/register", response_model=ResponseModel)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db_session)):
    try:
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        if not user.password:
            raise HTTPException(status_code=400, detail="Password is required")
        
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        user_data = create_user(db, user)
        
        return {
            "data": user_data,
            "message": "User created successfully, please wait for admin approval",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.post("/login", response_model=UserWithTokens)
def login_user(login: LoginRequest, db: Session = Depends(get_db_session)):
    
    try:
        user = db.query(User).filter((User.username == login.username) | (User.email == login.username)).first()
        
        if not user or not user.verify_password(login.password):
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")

        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# approved user by admin
@router.post("/{user_id}/approve", response_model=ApproveUser)
def approve_user(user_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin privileges required")
        
        user = db.query(User).filter(User.id == user_id).filter(User.deleted_at.is_(None)).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.is_admin:
            raise HTTPException(status_code=400, detail="Cannot approve an admin user")
        
        if user.is_admin_approved:
            user.is_admin_approved = False
        else:
            user.is_admin_approved = True
        
        db.commit()
        db.refresh(user)    
        
        return {
            "is_admin_approved": user.is_admin_approved,
            "message": "User approval status updated successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all user for the admin accees this APi 
@router.get("/all", response_model=list[UserOut])
def get_all_users_endpoint(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)  
):
    try:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin privileges required")
        users = get_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# user logout 
@router.post("/logout", response_model=dict)
def logout_user(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        # Delete all tokens for the current user
        db.query(Token).filter(Token.user_id == current_user.id).delete()
        db.commit()
        db.refresh(current_user)
        return {
            "message": "User logged out successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get all approved users
@router.get("/approved_user", response_model=list[UserOut])
def get_all_approved_users(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin privileges required")
        
        users = get_all_admin_approved_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all unapproved users
@router.get("/unapproved_users", response_model=list[UserOut])
def get_unapproved_users(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin privileges required")
        
        users = get_unapproved_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#  Get current user details
@router.get("/current_user_details", response_model=UserOut)
def get_current_user_details(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))