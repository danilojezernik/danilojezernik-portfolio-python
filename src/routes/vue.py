"""
Routes:
1. GET all typescript - Retrieve all typescript from the database.
2. GET Vue by ID - Retrieve a specific Vue by its ID.
3. GET limited typescript - Retrieve a limited number of typescript.
4. GET all typescript (private) - Retrieve all typescript for authenticated users.
5. GET Vue by ID (private) - Retrieve a specific Vue by its ID for authenticated users.
6. ADD a new Vue - Add a new Vue to the database.
7. EDIT a Vue by ID - Edit an existing Vue by its ID.
8. DELETE a Vue by ID - Delete a Vue by its ID.
"""
from fastapi import APIRouter, Depends, HTTPException

from src.domain.user import User
from src.domain.language import Language
from src.services import db
from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the typescript from the database
@router.get('/', operation_id='get_all_vue_public')
async def get_all_vue_public() -> list[Language]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of Vue objects containing all the typescript in the database
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.vue.find()

    # Create a list of Vue objects by unpacking data from each document retrieved
    vue_list = [Language(**document) for document in cursor]

    # Return the list of Vue objects
    return vue_list


# This route get one Vue by its ID
@router.get('/{_id}', operation_id='get_vue_by_id_public')
async def get_vue_by_id_public(_id: str):
    """
    This route handles the retrieval of one typescript by its ID from the database

    :param _id: The ID of the typescript to be retrieved
    :return: If the typescript is found, returns the typescript data; otherwise, returns a 404 error
    """

    # Attempt to find a typescript in the database based on the provided ID
    cursor = db.process.vue.find_one({'_id': _id})

    # If no typescript is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'typescript by ID: ({_id}) does not exist')
    else:

        # If the typescript is found, convert the cursor data into a typescript object and return it
        return Language(**cursor)


# This route gets a limited amount of typescript
@router.get('/limited/', operation_id='get_limited_typescript')
async def get_limited_typescript(limit: int = 4) -> list[Language]:
    """
    Handles the retrieval of a limited amount of typescript from the database.

    :param limit: The maximum number of typescript to retrieve (default is 2).
    :return: A list of typescript objects containing information about the limited typescript.
    """

    # Retrieve a limited number of typescript from the database using the limit method
    cursor = db.process.vue.find().limit(limit)

    # Create a list of Vue objects by unpacking data from each document retrieved
    typescript_limited_list = [Language(**document) for document in cursor]

    # Return the list of Vue objects
    return typescript_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the typescript from the database
@router.get('/admin/', operation_id='get_all_vue_private')
async def get_all_vue_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of Vue objects
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.vue.find()

    # Create a list of Vue objects by unpacking data from each document retrieved
    vue_list = [Language(**document) for document in cursor]

    # Return the list of Vue objects
    return vue_list


# This route get one Vue by its ID
@router.get('/admin/{_id}', operation_id='get_vue_by_id_private')
async def get_vue_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    This route handles the retrieval of one Vue by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the Vue to be retrieved
    :return: If the Vue is found, returns the Vue data; otherwise, returns a 404 error
    """

    # Attempt to find a Vue in the database based on the provided ID
    cursor = db.process.vue.find_one({'_id': _id})

    # If no Vue is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Vue by ID: ({_id}) does not exist')
    else:
        # If the Vue is found, convert the cursor data into a Vue object and return it
        return Language(**cursor)


# This route adds a new Vue
@router.post('/', operation_id='add_new_vue_private')
async def add_new_typescript(typescript: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the addition of a new Vue to the database.

    :param typescript: The Vue object representing the new Vue to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Vue object; otherwise, returns None.
    """

    # Convert the Vue object to a dictionary for database insertion
    typescript_dict = typescript.dict(by_alias=True)

    # Insert the Vue data into the database
    insert_result = db.process.vue.insert_one(typescript_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        typescript_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Vue object, using the updated dictionary
        return Language(**typescript_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a Vue by its ID
@router.put('/{_id}', operation_id='edit_vue_by_id_private')
async def edit_vue_by_id_private(_id: str, typescript: Language,
                                 current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the editing of a Vue by its ID in the database.

    :param _id: The ID of the Vue to be edited.
    :param typescript: The updated Vue object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Vue is successfully edited, returns the updated Vue object; otherwise, returns None.
    """

    # Convert the Vue object to a dictionary
    typescript_dict = typescript.dict(by_alias=True)

    # Delete the '_id' field from the Vue dictionary to avoid updating the ID
    del typescript_dict['_id']

    # Update the Vue in the database using the update_one method
    cursor = db.process.vue.update_one({'_id': _id}, {'$set': typescript_dict})

    # Check if the Vue was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated Vue from the database
        updated_document = db.process.vue.find_one({'_id': _id})

        # Check if the updated Vue exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Language(**updated_document)

    # Return None if the Vue was not updated
    return None


# Delete a Vue by its ID from the database
@router.delete('/{_id}', operation_id='delete_vue_by_id_private')
async def delete_vue_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a Vue by its ID from the database.

    :param _id: The ID of the Vue to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Vue is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the Vue from the database using the delete_one method
    delete_result = db.process.vue.delete_one({'_id': _id})

    # Check if the Vue was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Vue deleted successfully!'}
    else:
        # If the Vue was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Vue by ID: ({_id}) not found!')
