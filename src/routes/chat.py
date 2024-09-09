from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from src.services.connection_maneger import ConnectionManager

router = APIRouter()

# Instantiate the ConnectionManager to manage WebSocket connections and users
manager = ConnectionManager()


# Define a WebSocket endpoint for chat functionality
@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to handle real-time chatroom communication.
    Manages user connections, registration, and message broadcasting.

    Args:
        websocket (WebSocket): The WebSocket connection for the client.
    """

    # Establish the WebSocket connection and add it to the active connections
    await manager.connect(websocket)

    try:
        # First message received from the client should be the username
        username = await websocket.receive_text()

        # Register the user with the provided username
        await manager.register_user(websocket, username)

        # Keep listening for incoming messages from the client
        while True:
            # Receive a message from the connected client
            message = await websocket.receive_text()

            # Broadcast the received message to all other connected clients
            await manager.broadcast(message, manager.users[websocket])

    # Handle the case when the WebSocket connection is closed by the client
    except WebSocketDisconnect:
        # Clean up and remove the WebSocket connection from active users and connections
        manager.disconnect(websocket)
