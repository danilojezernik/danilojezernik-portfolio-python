"""
Routes:
1. GET all javascript - Retrieve all javascript from the database.
2. GET JavaScript by ID - Retrieve a specific JavaScript by its ID.
3. GET limited javascript - Retrieve a limited number of javascript.
4. GET all javascript (private) - Retrieve all javascript for authenticated users.
5. GET JavaScript by ID (private) - Retrieve a specific JavaScript by its ID for authenticated users.
6. ADD a new JavaScript - Add a new JavaScript to the database.
7. EDIT a JavaScript by ID - Edit an existing JavaScript by its ID.
8. DELETE a JavaScript by ID - Delete a JavaScript by its ID.
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


# This route gets all the javascript from the database
@router.get('/', operation_id='get_all_javascript_public')
async def get_all_javascript_public() -> list[Language]:
    """
    This route handles the retrieval of all the javascript from the database

    :return: a list of JavaScript objects containing all the javascript in the database
    """

    # Retrieve all javascript from the database using the find method
    cursor = db.process.javascript.find()

    # Create a list of JavaScript objects by unpacking data from each document retrieved
    javascript_list = [Language(**document) for document in cursor]

    # Return the list of JavaScript objects
    return javascript_list


# This route get one JavaScript by its ID
@router.get('/{_id}', operation_id='get_javascript_by_id_public')
async def get_javascript_by_id_public(_id: str):
    """
    This route handles the retrieval of one javascript by its ID from the database

    :param _id: The ID of the javascript to be retrieved
    :return: If the javascript is found, returns the javascript data; otherwise, returns a 404 error
    """

    # Attempt to find a javascript in the database based on the provided ID
    cursor = db.process.javascript.find_one({'_id': _id})

    # If no javascript is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'JavaScript by ID: ({_id}) does not exist')
    else:

        # If the javascript is found, convert the cursor data into a javascript object and return it
        return Language(**cursor)


# This route gets a limited amount of javascript
@router.get('/limited/', operation_id='get_limited_javascript')
async def get_limited_javascript(limit: int = 4) -> list[Language]:
    """
    Handles the retrieval of a limited amount of javascript from the database.

    :param limit: The maximum number of javascript to retrieve (default is 2).
    :return: A list of javascript objects containing information about the limited javascript.
    """

    # Retrieve a limited number of javascript from the database using the limit method
    cursor = db.process.javascript.find().limit(limit)

    # Create a list of JavaScript objects by unpacking data from each document retrieved
    javascript_limited_list = [Language(**document) for document in cursor]

    # Return the list of JavaScript objects
    return javascript_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the javascript from the database
@router.get('/admin/', operation_id='get_all_javascript_private')
async def get_all_javascript_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    This route handles the retrieval of all the javascript from the database

    :return: a list of JavaScript objects
    """

    # Retrieve all javascript from the database using the find method
    cursor = db.process.javascript.find()

    # Create a list of JavaScript objects by unpacking data from each document retrieved
    javascript_list = [Language(**document) for document in cursor]

    # Return the list of JavaScript objects
    return javascript_list


# This route get one JavaScript by its ID
@router.get('/admin/{_id}', operation_id='get_javascript_by_id_private')
async def get_javascript_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    This route handles the retrieval of one JavaScript by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the JavaScript to be retrieved
    :return: If the JavaScript is found, returns the JavaScript data; otherwise, returns a 404 error
    """

    # Attempt to find a JavaScript in the database based on the provided ID
    cursor = db.process.javascript.find_one({'_id': _id})

    # If no JavaScript is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'JavaScript by ID: ({_id}) does not exist')
    else:
        # If the JavaScript is found, convert the cursor data into a JavaScript object and return it
        return Language(**cursor)


# This route adds a new JavaScript
@router.post('/', operation_id='add_new_javascript_private')
async def add_new_javascript(javascript: Language,
                             current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the addition of a new JavaScript to the database.

    :param javascript: The JavaScript object representing the new JavaScript to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added JavaScript object; otherwise, returns None.
    """

    # Convert the JavaScript object to a dictionary for database insertion
    javascript_dict = javascript.dict(by_alias=True)

    # Insert the JavaScript data into the database
    insert_result = db.process.javascript.insert_one(javascript_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        javascript_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added JavaScript object, using the updated dictionary
        return Language(**javascript_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a JavaScript by its ID
@router.put('/{_id}', operation_id='edit_javascript_by_id_private')
async def edit_javascript_by_id_private(_id: str, javascript: Language,
                                        current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the editing of a JavaScript by its ID in the database.

    :param _id: The ID of the JavaScript to be edited.
    :param javascript: The updated JavaScript object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the JavaScript is successfully edited, returns the updated JavaScript object; otherwise, returns None.
    """

    # Convert the JavaScript object to a dictionary
    javascript_dict = javascript.dict(by_alias=True)

    # Delete the '_id' field from the JavaScript dictionary to avoid updating the ID
    del javascript_dict['_id']

    # Update the JavaScript in the database using the update_one method
    cursor = db.process.javascript.update_one({'_id': _id}, {'$set': javascript_dict})

    # Check if the JavaScript was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated JavaScript from the database
        updated_document = db.process.javascript.find_one({'_id': _id})

        # Check if the updated JavaScript exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Language(**updated_document)

    # Return None if the JavaScript was not updated
    return None


# Delete a JavaScript by its ID from the database
@router.delete('/{_id}', operation_id='delete_javascript_by_id_private')
async def delete_javascript_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a JavaScript by its ID from the database.

    :param _id: The ID of the JavaScript to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the JavaScript is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the JavaScript from the database using the delete_one method
    delete_result = db.process.javascript.delete_one({'_id': _id})

    # Check if the JavaScript was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'JavaScript deleted successfully!'}
    else:
        # If the JavaScript was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'JavaScript by ID: ({_id}) not found!')

