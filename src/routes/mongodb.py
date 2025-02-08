"""
Routes:
1. GET all mongodb - Retrieve all mongodb from the database.
2. GET MongoDb by ID - Retrieve a specific MongoDb by its ID.
3. GET limited mongodb - Retrieve a limited number of mongodb.
4. GET all mongodb (private) - Retrieve all mongodb for authenticated users.
5. GET MongoDb by ID (private) - Retrieve a specific MongoDb by its ID for authenticated users.
6. ADD a new MongoDb - Add a new MongoDb to the database.
7. EDIT a MongoDb by ID - Edit an existing MongoDb by its ID.
8. DELETE a MongoDb by ID - Delete a MongoDb by its ID.
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


# This route gets all the mongodb from the database
@router.get('/', operation_id='get_all_mongodb_public')
async def get_all_mongodb_public() -> list[Language]:
    """
    This route handles the retrieval of all the mongodb from the database

    :return: a list of MongoDb objects containing all the mongodb in the database
    """

    # Retrieve all mongodb from the database using the find method
    cursor = db.process.mongodb.find()

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_list = [Language(**document) for document in cursor]

    # Return the list of MongoDb objects
    return mongodb_list


# This route get one MongoDb by its ID
@router.get('/{_id}', operation_id='get_mongodb_by_id_public')
async def get_mongodb_by_id_public(_id: str):
    """
    This route handles the retrieval of one mongodb by its ID from the database

    :param _id: The ID of the mongodb to be retrieved
    :return: If the mongodb is found, returns the mongodb data; otherwise, returns a 404 error
    """

    # Attempt to find a mongodb in the database based on the provided ID
    cursor = db.process.mongodb.find_one({'_id': _id})

    # If no mongodb is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'mongodb by ID: ({_id}) does not exist')
    else:

        # If the mongodb is found, convert the cursor data into a mongodb object and return it
        return Language(**cursor)


# This route gets a limited amount of mongodb
@router.get('/limited/', operation_id='get_limited_mongodb')
async def get_limited_mongodb(limit: int = 4) -> list[Language]:
    """
    Handles the retrieval of a limited amount of mongodb from the database.

    :param limit: The maximum number of mongodb to retrieve (default is 2).
    :return: A list of mongodb objects containing information about the limited mongodb.
    """

    # Retrieve a limited number of mongodb from the database using the limit method
    cursor = db.process.mongodb.find().limit(limit)

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_limited_list = [Language(**document) for document in cursor]

    # Return the list of MongoDb objects
    return mongodb_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the mongodb from the database
@router.get('/admin/', operation_id='get_all_mongodb_private')
async def get_all_mongodb_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    This route handles the retrieval of all the mongodb from the database

    :return: a list of MongoDb objects
    """

    # Retrieve all mongodb from the database using the find method
    cursor = db.process.mongodb.find()

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_list = [Language(**document) for document in cursor]

    # Return the list of MongoDb objects
    return mongodb_list


# This route get one MongoDb by its ID
@router.get('/admin/{_id}', operation_id='get_mongodb_by_id_private')
async def get_mongodb_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    This route handles the retrieval of one MongoDb by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the MongoDb to be retrieved
    :return: If the MongoDb is found, returns the MongoDb data; otherwise, returns a 404 error
    """

    # Attempt to find a MongoDb in the database based on the provided ID
    cursor = db.process.mongodb.find_one({'_id': _id})

    # If no MongoDb is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'MongoDb by ID: ({_id}) does not exist')
    else:
        # If the MongoDb is found, convert the cursor data into a MongoDb object and return it
        return Language(**cursor)


# This route adds a new MongoDb
@router.post('/', operation_id='add_new_mongodb_private')
async def add_new_mongodb(mongodb: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the addition of a new MongoDb to the database.

    :param mongodb: The MongoDb object representing the new MongoDb to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added MongoDb object; otherwise, returns None.
    """

    # Convert the MongoDb object to a dictionary for database insertion
    mongodb_dict = mongodb.dict(by_alias=True)

    # Insert the MongoDb data into the database
    insert_result = db.process.mongodb.insert_one(mongodb_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        mongodb_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added MongoDb object, using the updated dictionary
        return Language(**mongodb_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a MongoDb by its ID
@router.put('/{_id}', operation_id='edit_mongodb_by_id_private')
async def edit_mongodb_by_id_private(_id: str, mongodb: Language,
                                     current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Handles the editing of a MongoDb by its ID in the database.

    :param _id: The ID of the MongoDb to be edited.
    :param mongodb The updated MongoDb object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the MongoDb is successfully edited, returns the updated MongoDb object; otherwise, returns None.
    """

    # Convert the MongoDb object to a dictionary
    mongodb_dict = mongodb.dict(by_alias=True)

    # Delete the '_id' field from the MongoDb dictionary to avoid updating the ID
    del mongodb_dict['_id']

    # Update the MongoDb in the database using the update_one method
    cursor = db.process.mongodb.update_one({'_id': _id}, {'$set': mongodb_dict})

    # Check if the MongoDb was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated MongoDb from the database
        updated_document = db.process.mongodb.find_one({'_id': _id})

        # Check if the updated MongoDb exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Language(**updated_document)

    # Return None if the MongoDb was not updated
    return None


# Delete a MongoDb by its ID from the database
@router.delete('/{_id}', operation_id='delete_mongodb_by_id_private')
async def delete_mongodb_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a MongoDb by its ID from the database.

    :param _id: The ID of the MongoDb to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the MongoDb is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the MongoDb from the database using the delete_one method
    delete_result = db.process.mongodb.delete_one({'_id': _id})

    # Check if the MongoDb was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'MongoDb deleted successfully!'}
    else:
        # If the MongoDb was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'MongoDb by ID: ({_id}) not found!')
