"""
Routes Overview:
1. GET / - Retrieves all users from the database (public).
2. GET /{_id} - Retrieves a user by their ID (public).
3. GET /admin/ - Retrieves all users from the database (private).
4. POST / - Adds a new user to the database (private).
5. GET /admin/{_id} - Retrieves a user by their ID (private).
6. PUT /{_id} - Edits a user by their ID (private).
7. DELETE /{_id} - Deletes a user by their ID (private).
"""

from fastapi import APIRouter, Depends

from src.domain.user import User
from src.services import db
from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all users from database
@router.get('/', operation_id='get_user_public')
async def get_user_public(current_user: User = Depends(get_current_user)) -> list[User]:
    """
    This route handles the retrieval of all the users from the database

    :return: a list of Users objects containing all the users in the database
    """

    # Retrieve all users from the database using the find method
    cursor = db.process.user.find()

    # Create a list of Users objects by unpacking data from each document retrieved
    user_list = [User(**document) for document in cursor]

    # Return the list of User objects
    return user_list
