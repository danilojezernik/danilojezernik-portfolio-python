from fastapi import APIRouter, Depends, HTTPException

from src.domain.user import User
from src.services import db
from src.services.security import get_current_user, pwd_context

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all users from database
@router.get('/', operation_id='get_user_public')
async def get_user_public() -> list[User]:
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
@router.get('/', operation_id='get_user_private')
async def get_user_private(current_user: str = Depends(get_current_user)) -> list[User]:
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


# Define a route for updating a user by ID - password is hashed when changed
@router.put('/{_id}', operation_id='edit_user_by_id')
async def edit_user_by_id(_id: str, user: User, current_user: str = Depends(get_current_user)) -> User | None:
    """
    Handles the editing of a user by its ID in the database.

    :param current_user: The current user, obtained from the authentication system.
    :param _id: The ID of the user to be edited.
    :param user: The updated User object with the new data.
    :return: If the user is successfully edited, returns the updated User object; otherwise, returns None.
    """

    # Check if the user wants to update the password
    if 'hashed_password' in user.dict(by_alias=True):
        # Hash the provided password using pwd_context.hash
        hashed_password = pwd_context.hash(user.dict(by_alias=True)['hashed_password'])
        user.dict()['hashed_password'] = hashed_password

    # Convert the user object to a dictionary with alias
    user_dict = user.dict(by_alias=True)

    # Remove '_id' from the dictionary as it shouldn't be updated
    del user_dict['_id']

    # Hash the password before updating the document in the database
    if 'hashed_password' in user_dict:
        user_dict['hashed_password'] = pwd_context.hash(user_dict['hashed_password'])

    # Update the user document in the database
    cursor = db.process.user.update_one({'_id': _id}, {'$set': user_dict})

    # Check if the user was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated user from the database
        updated_document = db.process.user.find_one({'_id': _id})

        # Check if the updated user exists
        if updated_document:
            # Convert the ObjectId to a string for the User model
            updated_document['_id'] = str(updated_document['_id'])
            # Create a User instance from the updated document
            return User(**updated_document)

    # Return None if the user was not updated
    return None


# Delete user by ID
@router.delete('/{_id}', operation_id='delete_user_by_id')
async def delete_user_by_id(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of a user by its ID from the database.

    :param _id: The ID of the user to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the user is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the blog from the database using the delete_one method
    delete_result = db.process.user.delete_one({'_id': _id})

    # Check if the blog was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'User deleted successfully'}
    else:
        # If the blog was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'User by ID: ({_id}) not found!')
