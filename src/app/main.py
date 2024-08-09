from fastapi import FastAPI
from app.db import db
from user.routes import register_user_routes
from signal.routes import register_signal_routes
from . import settings

app = FastAPI(title='SigConn SOS', docs_url='/docs')

register_user_routes(app)
register_signal_routes(app)