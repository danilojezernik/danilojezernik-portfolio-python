from fastapi import APIRouter, Depends, HTTPException

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


# Get user by ID
@router.get('/{_id}', operation_id='get_user_by_id')
async def get_user_by_id(_id: str, current_user: str = Depends(get_current_user)) -> User:
    """
    This route handles the retrieval of one user by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the user to be retrieved
    :return: If the user is found, returns the user data; otherwise, returns a 404 error
    """

    # Attempt to find a user in the database based on the provided ID
    cursor = db.process.user.find_one({'_id': _id})

    # If no user is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
    else:
        # If the user is found, convert the cursor data into a User object and return it
        return User(**cursor)


#