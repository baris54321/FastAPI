import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from models.token import Token
from db.session import get_db_session

# Load environment variables
load_dotenv()

# Read environment variables
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))  # 1 day default
SECRET_KEY = os.getenv("SECRET_KEY", "testsecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Decoded payload:", payload)
        return payload
    except ExpiredSignatureError:
        print("⛔ Token has expired.")
    except JWTError as e:
        print(f"⛔ Failed to decode token: {e}")
    return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)) -> User:
    
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token_exist = db.query(Token).filter((Token.access_token == token) | (Token.refresh_token == token)).first()
        if not token_exist:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        payload = decode_jwt_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        if "user_id" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user
    
    except HTTPException as e:
        raise  HTTPException(status_code=e.status_code, detail=e.detail)

if __name__ == "__main__":
    user_data = {"sub": "user@example.com", "role": "admin"}

    print("\n🔐 Generating tokens...")
    access_token = create_access_token(user_data.copy())
    refresh_token = create_refresh_token(user_data.copy())

    print("\n🪙 Access Token:\n", access_token)
    print("\n🌀 Refresh Token:\n", refresh_token)

    print("\n📥 Decoding Access Token:")
    decode_jwt_token(access_token)

    print("\n📥 Decoding Refresh Token:")
    decode_jwt_token(refresh_token)
