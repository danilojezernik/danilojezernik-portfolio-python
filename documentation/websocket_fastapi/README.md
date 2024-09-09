# Complete Backend Documentation for WebSocket Functionality in FastAPI

This documentation explains the WebSocket functionality built using FastAPI. It includes a detailed breakdown of the
code, covering every part of the backend WebSocket logic, its purpose, and how it works in real-time communication.

## Table of Contents:

1. **Introduction to WebSockets**
2. **Overview of the FastAPI WebSocket Setup**
3. `ConnectionManager` Class
    - `__init__()`
    - `connect(websocket: WebSocket)`
    - `disconnect(websocket: WebSocket)`
    - `broadcast(message: str, username: str)`
    - `register_user(websocket: WebSocket, username: str)`
    - `broadcast_user_join(username: str)`
4. **WebSocket Route** (`/ws/chat`)
5. **Error Handling**
6. **Flow Overview**
7. **Conclusion**

## 1. Introduction to WebSockets

WebSockets provide full-duplex communication between the server and clients over a single TCP connection. Unlike
traditional HTTP communication, where the client initiates every request, WebSockets allow the server to push messages
to clients at any time, enabling real-time interaction.

In this setup, we are using FastAPI to handle WebSocket connections, allowing multiple clients to join a chatroom, send
messages, and receive updates in real-time.

[WebSockets - FastAPI](https://fastapi.tiangolo.com/advanced/websockets/)

## 2. Overview of the FastAPI WebSocket Setup

The WebSocket functionality is managed by FastAPI's WebSocket endpoint. The system is built around the
`ConnectionManager` class, which handles connections, disconnections, broadcasting messages, and managing users in the
chatroom.

The WebSocket endpoint listens for incoming WebSocket connections, receives messages from clients, and broadcasts them
to other connected clients.

## 3. `ConnectionManager` Class

This class is responsible for managing active WebSocket connections, registering users, broadcasting messages, and
handling disconnections.

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: dict[WebSocket, str] = {}
```

**Purpose:**

- **active_connections**: A list to track all currently active WebSocket connections.
- **users**: A dictionary mapping each active WebSocket to the associated username. This ensures that messages are
  associated with the correct user.

### Detailed Breakdown of Methods

### `connect(websocket: WebSocket)`

```python
async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.active_connections.append(websocket)
```

**Purpose:**

- This method accepts a new WebSocket connection from a client.
- It first calls `websocket.accept()` to formally establish the connection and then appends the connection to the
  `active_connections` list.

**Why is it necessary?**

- Every time a new client joins the chat, this method is called to ensure the connection is recognized and stored for
  future communication.

### `disconnect(websocket: WebSocket)`

```python
def disconnect(self, websocket: WebSocket):
    if websocket in self.active_connections:
        self.active_connections.remove(websocket)
    if websocket in self.users:
        del self.users[websocket]
```

**Purpose:**

- This method handles the removal of a WebSocket connection when a client disconnects.
- It removes the connection from `active_connections` and deletes any associated username from the `users` dictionary.

**Why is it necessary?**

- When a client leaves the chat or their connection closes unexpectedly, the WebSocket must be removed to ensure that
  messages aren't sent to non-existent connections.

### `broadcast(message: str, username: str)`

```python
async def broadcast(self, message: str, username: str):
    message_data = {"username": username, "message": message}
    for connection in self.active_connections:
        try:
            await connection.send_text(json.dumps(message_data))
        except Exception:
            self.disconnect(connection)
```

**Purpose:**

- This method sends a message from one user to all other connected clients.
- It loops through all active connections and sends the message to each one in JSON format.

**Why is it necessary?**

- Broadcasting is essential for real-time communication in the chatroom, as it allows a message sent by one user to be
  delivered to every other user.

**Error Handling:**

- If an error occurs while sending the message (e.g., a client has disconnected unexpectedly), the method calls
  `disconnect()` to clean up the broken connection.

### `register_user(websocket: WebSocket, username: str)`

```python
async def register_user(self, websocket: WebSocket, username: str):
    if username in self.users.values():
        await websocket.send_text(json.dumps({"error": "Username already taken"}))
        await websocket.close()
        self.disconnect(websocket)
    else:
        self.users[websocket] = username
        await self.broadcast_user_join(username)
```

**Purpose:**

- This method is responsible for registering a new user with a unique username.
- It checks whether the username is already taken and either:
    - Rejects the user if the username is taken by closing the WebSocket, or
    - Registers the user and broadcasts the "user has joined" message to all other clients.

**Why is it necessary?**

- This ensures that each user in the chatroom has a unique identifier and allows clients to know when a new user has
  joined.

### `broadcast_user_join(username: str)`

```python
async def broadcast_user_join(self, username: str):
    message_data = {"username": username, "message": f"{username} has joined the chat"}
    for connection in self.active_connections:
        try:
            await connection.send_text(json.dumps(message_data))
        except Exception:
            self.disconnect(connection)
```

**Purpose:**

- This method broadcasts a message to all clients notifying them when a new user successfully joins the chat.

**Why is it necessary?**

- It's important for users to see when others join the chatroom in real time, creating an engaging and interactive
  environment.

## 4. WebSocket Route (/ws/chat)

```python
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from src.services.connection_maneger import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # First message from client should be the username
        username = await websocket.receive_text()
        await manager.register_user(websocket, username)

        # Continue receiving messages
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(message, manager.users[websocket])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Purpose:**

- This defines the `/ws/chat` WebSocket endpoint where clients can connect to the chatroom.

**Detailed Breakdown:**

1. `await manager.connect(websocket)`: When a new client connects, the `connect()` method is called to establish the
   WebSocket connection.
2. Receiving the Username:
    - The first message sent by the client is expected to be the username, which is handled by
      `await websocket.receive_text()`.
    - The `register_user()` method checks if the username is valid and registers the user.
3. Receiving and Broadcasting Messages:
    - Once the username is registered, the server enters an infinite loop (`while True`) to continuously receive
      messages
      from the client and broadcast them to all other clients.
4. Handling Disconnects:
   -If a client disconnects, the `WebSocketDisconnect` exception is caught, and the `disconnect()` method is called to
   clean
   up the connection.

## 5. Error Handling

1. Duplicate Usernames:
    - If a user attempts to join with a username that is already in use, the server sends an error message (
      `{"error": "Username already taken"}`) and immediately closes the connection.
    - This prevents duplicate users and ensures each user has a unique identity in the chatroom.

2. Failed Connections:
    - If a connection fails while sending messages (e.g., a user disconnects), the server will call `disconnect()` to
      clean up and prevent further attempts to send messages to that WebSocket.

## 6. Flow Overview

1. **Client Connects**: A WebSocket connection is established when the client connects to `/ws/chat`.
2. **Username Registration**: The client sends a username. If it's unique, the user is registered; otherwise, the
   connection is closed.
3. **Message Handling**: The client can send messages, which are broadcasted to all other clients.
4. **Disconnection**: If the client disconnects, the server removes them from the chatroom and stops sending them
   messages.

## 7. Conclusion

This WebSocket setup in FastAPI allows for a real-time chatroom with multiple clients. The `ConnectionManager` class
handles the lifecycle of each WebSocket connection, from establishing a connection, to broadcasting messages, to
handling disconnections. This design ensures that each user has a unique identity in the chat, and provides robust error
handling for unexpected disconnections or failed message deliveries.