from fastapi import FastAPI, HTTPException, Depends
import jwt
from app.db import db
from src.app import settings
from .models import LoginRequest,SignUpRequest, TokenData
from helpers.authorization import get_password_hash, authenticate_user, create_access_token, get_user, get_user_from_token
from typing import Annotated, Union
from helpers.authorization import oauth2_scheme

def register_user_routes(app: FastAPI):
    @app.post('/login')
    async def login(request: LoginRequest):
        user = authenticate_user(request.username, request.password)
        if user:
            return {
                    'message': 'Login successfully',
                    'access_token': create_access_token(
                        data={'username': user['username']}, 
                        expires_delta=None
                    )
                }
        return {'message': 'Wrong username or password'}
    
    @app.post('/signup')
    async def signup(request: SignUpRequest):
        try:
            data = dict(request)
            data['password'] = get_password_hash(data['password'])
            data['role'] = 'user'
            print(data)
            db['users'].insert_one(data)
            return {'message': 'Signup successfully'}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.get('/current-user')
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        print(token)
        return get_user_from_token(token)