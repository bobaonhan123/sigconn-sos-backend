from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import db
from user.routes import register_user_routes
from sos_signal.routes import register_signal_routes
from . import settings

app = FastAPI(title='SigConn SOS', docs_url='/docs')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_user_routes(app)
register_signal_routes(app)