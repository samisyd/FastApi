from datetime import timedelta, datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import get_db, DbSession, SessionLocal
from models import User
# from passlib.context import CryptContext
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
# import logging
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the password hasher
password_hash = PasswordHash.recommended()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# You would want to store this in an environment variable or a secret manager
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# api endpoint to create a new user
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
# this is used to hash the password when creating a user and to verify the password when logging in , password hashing and verification is important for security reasons
# bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserRequest, db: db_dependency):
    # Check if the username or email already exists
    #  
    # Hash the password before storing it in the database
    # user.password = user.password.strip()  # Remove leading/trailing whitespace
    # user.password = user.password[:72]  # Limit password length to 72 characters
    # # To hash a password (e.g., during registration)
    hashed_password = password_hash.hash(user.password)
    # hashed_password = bcrypt_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/token", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(db, form_data.username, form_data.password)    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    # Create a JWT token for the authenticated user
    # jwt web token creation valid for 30 minutes. You can adjust the expiration time as needed.    
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))    
       
    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    to_encode = {"sub": username, "user_id": user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: DbSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user