from typing import Annotated
import os
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
#import pydantic to create your models
from pydantic import BaseModel, Field, EmailStr
from fastapi import Depends, FastAPI, Form, HTTPException, status
from models.user_model import User, UserBody
from fastapi.security import OAuth2PasswordBearer
from config.db_config import accounts
import jwt
from jwt.exceptions import InvalidTokenError

#ENVs
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class UserInDB(User):
    password: str

#initiate encryption
enc_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#instance of the bearer token
outh2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/aller-manger/v1.0/users/login'
)

#get user from the db
def get_user(username: str):
    user_info = accounts.find_one({"user_name":username})

    if not user_info:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Login failed, no user found."
        )
    
    return UserInDB(**user_info)

#authenticate login
def authenticate_user(uname: str, upass:str):
    user = accounts.find_one({"user_name":uname})

    if not user:
        return False
    
    hash_pass = user.get("password")

    if not verify_password(upass, hash_pass):
        return False
    
    return UserBody(
        user_name= user.get("user_name"),
        user_id= user.get("user_id"),
        email= user.get("email"),
        phone= user.get("phone"),
        first_name= user.get("first_name"),
        last_name= user.get("last_name")

    ).model_dump()

def verify_password(plain_txt, hashed_txt):

    return enc_context.verify(plain_txt, hashed_txt)

def encrypt_password(plainPassword):
    return enc_context.hash(plainPassword)

#creating access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer)]):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate info.",
        headers={"WWW-Authenticated":"Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        if not payload.get("user_name"):
            raise credentials_exception
        
        token_data = UserBody(
        user_name= payload.get("user_name"),
        user_id= payload.get("user_id"),
        email= payload.get("email"),
        phone= payload.get("phone"),
        first_name= payload.get("first_name"),
        last_name= payload.get("last_name")

        )
    except InvalidTokenError:
        raise credentials_exception
    
    #get user
    user =  get_user(username=token_data.user_name)

    if user is None:
        raise credentials_exception
    
    return user