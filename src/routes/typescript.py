"""
Routes:
1. GET all typescript - Retrieve all typescript from the database.
2. GET TypeScript by ID - Retrieve a specific TypeScript by its ID.
3. GET limited typescript - Retrieve a limited number of typescript.
4. GET all typescript (private) - Retrieve all typescript for authenticated users.
5. GET TypeScript by ID (private) - Retrieve a specific TypeScript by its ID for authenticated users.
6. ADD a new TypeScript - Add a new TypeScript to the database.
7. EDIT a TypeScript by ID - Edit an existing TypeScript by its ID.
8. DELETE a TypeScript by ID - Delete a TypeScript by its ID.
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


# This route gets all the typescript from the database
@router.get('/', operation_id='get_all_typescript_public')
async def get_all_typescript_public() -> list[Language]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of TypeScript objects containing all the typescript in the database
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.typescript.find()

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_list = [Language(**document) for document in cursor]

    # Return the list of TypeScript objects
    return typescript_list


# This route get one TypeScript by its ID
@router.get('/{_id}', operation_id='get_typescript_by_id_public')
async def get_typescript_by_id_public(_id: str):
    """
    This route handles the retrieval of one typescript by its ID from the database

    :param _id: The ID of the typescript to be retrieved
    :return: If the typescript is found, returns the typescript data; otherwise, returns a 404 error
    """

    # Attempt to find a typescript in the database based on the provided ID
    cursor = db.process.typescript.find_one({'_id': _id})

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
    cursor = db.process.typescript.find().limit(limit)

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_limited_list = [Language(**document) for document in cursor]

    # Return the list of TypeScript objects
    return typescript_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the typescript from the database
@router.get('/admin/', operation_id='get_all_typescript_private')
async def get_all_typescript_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of TypeScript objects
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.typescript.find()

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_list = [Language(**document) for document in cursor]

    # Return the list of TypeScript objects
    return typescript_list


# This route get one TypeScript by its ID
@router.get('/admin/{_id}', operation_id='get_typescript_by_id_private')
async def get_typescript_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    This route handles the retrieval of one TypeScript by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the TypeScript to be retrieved
    :return: If the TypeScript is found, returns the TypeScript data; otherwise, returns a 404 error
    """

    # Attempt to find a TypeScript in the database based on the provided ID
    cursor = db.process.typescript.find_one({'_id': _id})

    # If no TypeScript is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'TypeScript by ID: ({_id}) does not exist')
    else:
        # If the TypeScript is found, convert the cursor data into a TypeScript object and return it
        return Language(**cursor)


# This route adds a new TypeScript
@router.post('/', operation_id='add_new_typescript_private')
async def add_new_typescript(typescript: Language,
                             current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the addition of a new TypeScript to the database.

    :param typescript: The TypeScript object representing the new TypeScript to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added TypeScript object; otherwise, returns None.
    """

    # Convert the TypeScript object to a dictionary for database insertion
    typescript_dict = typescript.dict(by_alias=True)

    # Insert the TypeScript data into the database
    insert_result = db.process.typescript.insert_one(typescript_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        typescript_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added TypeScript object, using the updated dictionary
        return Language(**typescript_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a TypeScript by its ID
@router.put('/{_id}', operation_id='edit_typescript_by_id_private')
async def edit_typescript_by_id_private(_id: str, typescript: Language,
                                        current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the editing of a TypeScript by its ID in the database.

    :param _id: The ID of the TypeScript to be edited.
    :param typescript: The updated TypeScript object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the TypeScript is successfully edited, returns the updated TypeScript object; otherwise, returns None.
    """

    # Convert the TypeScript object to a dictionary
    typescript_dict = typescript.dict(by_alias=True)

    # Delete the '_id' field from the TypeScript dictionary to avoid updating the ID
    del typescript_dict['_id']

    # Update the TypeScript in the database using the update_one method
    cursor = db.process.typescript.update_one({'_id': _id}, {'$set': typescript_dict})

    # Check if the TypeScript was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated TypeScript from the database
        updated_document = db.process.typescript.find_one({'_id': _id})

        # Check if the updated TypeScript exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Language(**updated_document)

    # Return None if the TypeScript was not updated
    return None


# Delete a TypeScript by its ID from the database
@router.delete('/{_id}', operation_id='delete_typescript_by_id_private')
async def delete_typescript_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a TypeScript by its ID from the database.

    :param _id: The ID of the TypeScript to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the TypeScript is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the TypeScript from the database using the delete_one method
    delete_result = db.process.typescript.delete_one({'_id': _id})

    # Check if the TypeScript was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'TypeScript deleted successfully!'}
    else:
        # If the TypeScript was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'TypeScript by ID: ({_id}) not found!')
