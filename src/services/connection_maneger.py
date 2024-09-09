import json
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections and users in a chatroom.
    Handles connecting, disconnecting, broadcasting messages, and user registration.
    """

    def __init__(self):
        """
        Initializes the ConnectionManager with:
        - active_connections: A list of currently connected WebSocket clients.
        - users: A dictionary mapping WebSocket connections to usernames.
        """
        self.active_connections: List[WebSocket] = []  # List to store active WebSocket connections
        self.users: dict[WebSocket, str] = {}  # Dictionary to map WebSocket to associated username

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection and adds it to the list of active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to be accepted and tracked.
        """
        await websocket.accept()  # Accept the incoming WebSocket connection
        self.active_connections.append(websocket)  # Add the WebSocket connection to the active list

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections and deletes associated user.

        Args:
            websocket (WebSocket): The WebSocket connection to be removed.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)  # Remove WebSocket connection from active list
        if websocket in self.users:
            del self.users[websocket]  # Remove associated user from the dictionary if present

    async def broadcast(self, message: str, username: str):
        """
        Broadcasts a message to all active WebSocket connections.

        Args:
            message (str): The message to be broadcasted.
            username (str): The username of the sender.
        """
        message_data = {"username": username, "message": message}  # Prepare the message payload
        for connection in self.active_connections:
            try:
                # Send the message to each active WebSocket connection
                await connection.send_text(json.dumps(message_data))
            except Exception:
                # If sending fails (e.g., connection closed), remove the WebSocket connection
                self.disconnect(connection)

    async def register_user(self, websocket: WebSocket, username: str):
        """
        Registers a new user to the WebSocket connection if the username is not already taken.

        Args:
            websocket (WebSocket): The WebSocket connection to be associated with the username.
            username (str): The username to be registered.
        """
        # Check if the username is already in use by any other connection
        if username in self.users.values():
            # Notify the user that the username is already taken
            await websocket.send_text(json.dumps({"error": "Username already taken"}))
            # Close the WebSocket connection after notifying the user
            await websocket.close()
            self.disconnect(websocket)  # Clean up the WebSocket connection
        else:
            # Register the user if the username is unique
            self.users[websocket] = username
            # Notify all users that a new user has joined the chat
            await self.broadcast_user_join(username)

    async def broadcast_user_join(self, username: str):
        """
        Broadcasts a message to all users when a new user joins the chat.

        Args:
            username (str): The username of the user who joined.
        """
        message_data = {"username": username, "message": f"{username} has joined the chat"}
        # Send the "user has joined" message to all active WebSocket connections
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message_data))
            except Exception:
                # Handle potential exceptions by disconnecting the problematic connection
                self.disconnect(connection)
