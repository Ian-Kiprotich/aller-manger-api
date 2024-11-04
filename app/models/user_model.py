#import pydantic to create your models
from pydantic import BaseModel, Field, EmailStr
#uuid
from uuid import uuid4

#for automatically creating the date
from datetime import datetime

#user account class
class User(BaseModel):
    user_id: str = str(uuid4())
    user_name: str 
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str

class UserLoginRequest(BaseModel):
    user_name: str
    password: str

class UserBody(BaseModel):
    user_name: str 
    user_id: str
    email: EmailStr
    phone: str
    first_name: str
    last_name: str
    