from fastapi import WebSocket
from .models import UserSocket
from typing import Dict, List

class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []
 
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
 
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
 
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
         
    async def broadcast(self, message: dict, websocket: WebSocket):
        for connection in self.active_connections:
            if(connection == websocket):
                continue
            await connection.send_json(message)
            
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)
            
class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, List[UserSocket]] = {}

    async def connect(self, websocket: WebSocket, username: str, signal_id: str):
        await websocket.accept()
        if signal_id not in self.active_connections:
            self.active_connections[signal_id] = []
        self.active_connections[signal_id].append(UserSocket(username=username, websocket=websocket))

    def disconnect(self, websocket: WebSocket, signal_id: str):
        if signal_id in self.active_connections:
            self.active_connections[signal_id] = [
                user for user in self.active_connections[signal_id]
                if user.websocket != websocket
            ]
            if not self.active_connections[signal_id]:  # Remove the entry if no users left
                del self.active_connections[signal_id]

    async def broadcast(self, message: dict, signal_id: str):
        if signal_id in self.active_connections:
            for user in self.active_connections[signal_id]:
                await user.websocket.send_json(message)
    

connection_manager = ConnectionManager()
chat_manager = ChatManager()
