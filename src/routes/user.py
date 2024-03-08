from fastapi import APIRouter, Depends

from src.domain.user import User
from src.services import db
from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all users from database
@router.get('/')
async def get_user() -> list[User]:
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


"""
THIS ROUTES ARE PRIVATE
"""


# Get all users from database
@router.get('/')
async def get_user(current_user: str = Depends(get_current_user)) -> list[User]:
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
