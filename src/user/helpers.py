from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Any

from fastapi import Depends, HTTPException
from app import settings
import jwt
from passlib.context import CryptContext
from app.db import db
from fastapi.security import OAuth2PasswordBearer

from src.user.models import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                             settings.SECRET_KEY, 
                             algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    user = db['users'].find_one({'username': username})
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

def get_user(username: str):
    user = db['users'].find_one({'username': username})
    user['id'] = str(user['_id'])
    return user

def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, 
                                algorithms=[settings.SECURITY_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    user.pop('password')
    user.pop('_id')
    return user