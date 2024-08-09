from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    username: str
    password: str
    phone_number: str
    full_name: str

class User(BaseModel):
    username: str
    password: str
    phone_number: str
    full_name: str
    role: str