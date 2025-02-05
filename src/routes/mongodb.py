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
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.mongodb import MongoDb
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user

# Define the root media directory and the subdirectory for media files
mongodb_root_directory = 'media'  # The root directory where all media files are stored
media_directory = os.path.join(mongodb_root_directory, 'mongodb_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the mongodb from the database
@router.get('/', operation_id='get_all_mongodb_public')
async def get_all_mongodb_public() -> list[MongoDb]:
    """
    This route handles the retrieval of all the mongodb from the database

    :return: a list of MongoDb objects containing all the mongodb in the database
    """

    # Retrieve all mongodb from the database using the find method
    cursor = db.process.mongodb.find()

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_list = [MongoDb(**document) for document in cursor]

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
        return MongoDb(**cursor)


# This route gets a limited amount of mongodb
@router.get('/limited/', operation_id='get_limited_mongodb')
async def get_limited_mongodb(limit: int = 4) -> list[MongoDb]:
    """
    Handles the retrieval of a limited amount of mongodb from the database.

    :param limit: The maximum number of mongodb to retrieve (default is 2).
    :return: A list of mongodb objects containing information about the limited mongodb.
    """

    # Retrieve a limited number of mongodb from the database using the limit method
    cursor = db.process.mongodb.find().limit(limit)

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_limited_list = [MongoDb(**document) for document in cursor]

    # Return the list of MongoDb objects
    return mongodb_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the mongodb from the database
@router.get('/admin/', operation_id='get_all_mongodb_private')
async def get_all_mongodb_private(current_user: User = Depends(get_current_user)) -> list[MongoDb]:
    """
    This route handles the retrieval of all the mongodb from the database

    :return: a list of MongoDb objects
    """

    # Retrieve all mongodb from the database using the find method
    cursor = db.process.mongodb.find()

    # Create a list of MongoDb objects by unpacking data from each document retrieved
    mongodb_list = [MongoDb(**document) for document in cursor]

    # Return the list of MongoDb objects
    return mongodb_list


# This route get one MongoDb by its ID
@router.get('/admin/{_id}', operation_id='get_mongodb_by_id_private')
async def get_mongodb_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> MongoDb:
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
        return MongoDb(**cursor)


# This route adds a new MongoDb
@router.post('/', operation_id='add_new_mongodb_private')
async def add_new_mongodb(mongodb: MongoDb, current_user: User = Depends(get_current_user)) -> MongoDb | None:
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
        return MongoDb(**mongodb_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a MongoDb by its ID
@router.put('/{_id}', operation_id='edit_mongodb_by_id_private')
async def edit_mongodb_by_id_private(_id: str, mongodb: MongoDb,
                                     current_user: User = Depends(get_current_user)) -> MongoDb | None:
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
            return MongoDb(**updated_document)

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


"""
Media Routes:
1. POST / - Upload a media file.
2. GET /{filename} - Retrieve a media file by filename.
3. GET /images/ - List all media files.
4. DELETE /{filename} - Delete a media file by filename.
"""


# PUBLIC

# Retrieve a media file by filename
@router.get('/media/{filename}')
async def get_mongodb_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(media_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Raise a 404 error if the file is not found
        return {"message": f"Image '{filename}' not found in the directory."}

    try:
        # Return the file as a response
        return FileResponse(file_path)
    except Exception as e:
        # Raise an HTTP 500 error if there was an issue serving the file
        return {"message": f"Error serving file: {str(e)}"}


# PRIVATE

# Upload a media file
@router.post("/media/")
async def upload_mongodb_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Upload a media file to the server.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        os.makedirs(media_directory, exist_ok=True)
        contents = await file.read()
        file_name = file.filename if file.filename else 'uploaded_file'
        file_path = os.path.join(media_directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'There was an error uploading the file: {str(e)}')
    finally:
        await file.close()
    return {"message": f"Successfully uploaded {file_name} to {media_directory}"}


# List all media files
@router.get('/images/')
async def list_mongodb_images(current_user: User = Depends(get_current_user)):
    """
    List all media files in the upload directory.

    :return: A list of filenames in the upload directory.
    """
    if not os.path.exists(media_directory):
        return {"images": [], "message": "No images found. Directory does not exist."}

    image_names = [f for f in os.listdir(media_directory) if os.path.isfile(os.path.join(media_directory, f))]
    # If no images are found, return an empty list with a message
    if not image_names:
        return {"images": [], "message": "No images found in the directory."}

    # Return the list of filenames
    return {"images": image_names}


# Delete a media file by filename
@router.delete("/media/{filename}")
async def delete_mongodb_image(filename: str, current_user: User = Depends(get_current_user)):
    """
    Delete a media file from the upload directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    file_path = os.path.join(media_directory, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")
    return {"message": f"Successfully deleted {filename} from {media_directory}"}
