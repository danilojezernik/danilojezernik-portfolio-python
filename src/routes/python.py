"""
Routes:
1. GET all python - Retrieve all python from the database.
2. GET Python by ID - Retrieve a specific Python by its ID.
3. GET limited python - Retrieve a limited number of python.
4. GET all python (private) - Retrieve all python for authenticated users.
5. GET Python by ID (private) - Retrieve a specific Python by its ID for authenticated users.
6. ADD a new Python - Add a new Python to the database.
7. EDIT a Python by ID - Edit an existing Python by its ID.
8. DELETE a Python by ID - Delete a Python by its ID.
"""
from fastapi import APIRouter, Depends, HTTPException

from src.domain.language import Language
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the python from the database
@router.get('/', operation_id='get_all_python_public')
async def get_all_python_public() -> list[Language]:
    """
    This route handles the retrieval of all the python from the database

    :return: a list of Python objects containing all the python in the database
    """

    # Retrieve all python from the database using the find method
    cursor = db.process.python.find()

    # Create a list of Python objects by unpacking data from each document retrieved
    python_list = [Language(**document) for document in cursor]

    # Return the list of Python objects
    return python_list


# This route get one Python by its ID
@router.get('/{_id}', operation_id='get_python_by_id_public')
async def get_python_by_id_public(_id: str):
    """
    This route handles the retrieval of one python by its ID from the database

    :param _id: The ID of the python to be retrieved
    :return: If the python is found, returns the python data; otherwise, returns a 404 error
    """

    # Attempt to find a python in the database based on the provided ID
    cursor = db.process.python.find_one({'_id': _id})

    # If no python is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'python by ID: ({_id}) does not exist')
    else:

        # If the python is found, convert the cursor data into a python object and return it
        return Language(**cursor)


# This route gets a limited amount of python
@router.get('/limited/', operation_id='get_limited_python')
async def get_limited_python(limit: int = 4) -> list[Language]:
    """
    Handles the retrieval of a limited amount of python from the database.

    :param limit: The maximum number of python to retrieve (default is 2).
    :return: A list of python objects containing information about the limited python.
    """

    # Retrieve a limited number of python from the database using the limit method
    cursor = db.process.python.find().limit(limit)

    # Create a list of Python objects by unpacking data from each document retrieved
    python_limited_list = [Language(**document) for document in cursor]

    # Return the list of Python objects
    return python_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the python from the database
@router.get('/admin/', operation_id='get_all_python_private')
async def get_all_python_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    This route handles the retrieval of all the python from the database

    :return: a list of Python objects
    """

    # Retrieve all python from the database using the find method
    cursor = db.process.python.find()

    # Create a list of Python objects by unpacking data from each document retrieved
    python_list = [Language(**document) for document in cursor]

    # Return the list of Python objects
    return python_list


# This route get one Python by its ID
@router.get('/admin/{_id}', operation_id='get_python_by_id_private')
async def get_python_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    This route handles the retrieval of one Python by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the Python to be retrieved
    :return: If the Python is found, returns the Python data; otherwise, returns a 404 error
    """

    # Attempt to find a Python in the database based on the provided ID
    cursor = db.process.python.find_one({'_id': _id})

    # If no Python is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Python by ID: ({_id}) does not exist')
    else:
        # If the Python is found, convert the cursor data into a Python object and return it
        return Language(**cursor)


# This route adds a new Python
@router.post('/', operation_id='add_new_python_private')
async def add_new_python(python: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the addition of a new Python to the database.

    :param python: The Python object representing the new Python to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Python object; otherwise, returns None.
    """

    # Convert the Python object to a dictionary for database insertion
    python_dict = python.dict(by_alias=True)

    # Insert the Python data into the database
    insert_result = db.process.python.insert_one(python_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        python_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Python object, using the updated dictionary
        return Language(**python_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a Python by its ID
@router.put('/{_id}', operation_id='edit_python_by_id_private')
async def edit_python_by_id_private(_id: str, python: Language,
                                    current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the editing of a Python by its ID in the database.

    :param _id: The ID of the Python to be edited.
    :param python: The updated Python object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Python is successfully edited, returns the updated Python object; otherwise, returns None.
    """

    # Convert the Python object to a dictionary
    python_dict = python.dict(by_alias=True)

    # Delete the '_id' field from the Python dictionary to avoid updating the ID
    del python_dict['_id']

    # Update the Python in the database using the update_one method
    cursor = db.process.python.update_one({'_id': _id}, {'$set': python_dict})

    # Check if the Python was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated Python from the database
        updated_document = db.process.python.find_one({'_id': _id})

        # Check if the updated Python exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Language(**updated_document)

    # Return None if the Python was not updated
    return None


# Delete a Python by its ID from the database
@router.delete('/{_id}', operation_id='delete_python_by_id_private')
async def delete_python_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a Python by its ID from the database.

    :param _id: The ID of the Python to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Python is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the Python from the database using the delete_one method
    delete_result = db.process.python.delete_one({'_id': _id})

    # Check if the Python was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Python deleted successfully!'}
    else:
        # If the Python was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Python by ID: ({_id}) not found!')
