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

#initiate encryption context
enc_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
#initiate an instance of the bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/aller-manger/v1.0/users/login")


#get user from db
def get_user(username: str):
     #fetch user from accounts
    user_info = accounts.find_one({"user_name":username})
    
    #check for body
    if not user_info:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Login failed, could not find guest."
        )
    
    return UserInDB(**user_info)
    
    
    
#authenticate at login
def authenticate_user(uname: str, upass: str):
    user = accounts.find_one({"user_name":uname})
    if not user:
        return False
    
    #get user info password
    hashed_pass = user.get("password")
    if not verify_password(upass, hashed_pass):
        return False
   
    return UserBody(
        user_name=user.get("user_name"),
        user_id=user.get("user_id"),
        email=user.get("email"),
        phone=user.get("phone"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name")
    ).model_dump()
       

#to verify login
def verify_password(plain_txt, hashed_txt):
    return enc_context.verify(plain_txt, hashed_txt)

#to create hashes
def encrypt_password(plain_txt):
    return enc_context.hash(plain_txt)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    #set the token expiry time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    #create the access token here
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#get the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
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
    user = get_user(username=token_data.user_name)
    if user is None:
        raise credentials_exception
    
    return user