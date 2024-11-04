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

