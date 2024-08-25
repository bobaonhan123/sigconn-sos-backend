from fastapi import WebSocket
from pydantic import BaseModel

class SignalRequest(BaseModel):
    latitude: float
    longitude: float
    message: str

class ChatMessage(BaseModel):
    username: str
    message: str
    type: str
    
class UserSocket:
    username: str
    websocket: WebSocket
    def __init__(self, username: str, websocket: WebSocket):
        self.username = username
        self.websocket = websocket