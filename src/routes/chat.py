from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from typing import List

from src.domain.user import User
from src.services.security import get_current_user

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.users:
            del self.users[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_user_join(self, username: str):
        await self.broadcast(f"{username} has joined the chat")

    async def register_user(self, websocket: WebSocket, username: str):
        self.users[websocket] = username
        await self.broadcast_user_join(username)


manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, current_user: User = Depends(get_current_user)):
    await manager.connect(websocket)
    try:
        # First message from client should be the username
        username = await websocket.receive_text()
        await manager.register_user(websocket, username)

        # Then continue receiving messages
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{manager.users[websocket]}: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
