"""
Routes:
1. GET all angular - Retrieve all angular from the database.
2. GET Angular by ID - Retrieve a specific Angular by its ID.
3. GET limited angular - Retrieve a limited number of angular.
4. GET all angular (private) - Retrieve all angular for authenticated users.
5. GET Angular by ID (private) - Retrieve a specific Angular by its ID for authenticated users.
6. ADD a new Angular - Add a new Angular to the database.
7. EDIT a Angular by ID - Edit an existing Angular by its ID.
8. DELETE a Angular by ID - Delete a Angular by its ID.
"""
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.angular import Angular
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user

# Define the root media directory and the subdirectory for media files
angular_root_directory = 'media'  # The root directory where all media files are stored
media_directory = os.path.join(angular_root_directory, 'angular_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the angular from the database
@router.get('/', operation_id='get_all_angular_public')
async def get_all_angular_public() -> list[Angular]:
    """
    This route handles the retrieval of all the angular from the database

    :return: a list of Angular objects containing all the angular in the database
    """

    # Retrieve all angular from the database using the find method
    cursor = db.process.angular.find()

    # Create a list of Angular objects by unpacking data from each document retrieved
    angular_list = [Angular(**document) for document in cursor]

    # Return the list of Angular objects
    return angular_list


# This route get one Angular by its ID
@router.get('/{_id}', operation_id='get_angular_by_id_public')
async def get_angular_by_id_public(_id: str):
    """
    This route handles the retrieval of one angular by its ID from the database

    :param _id: The ID of the angular to be retrieved
    :return: If the angular is found, returns the angular data; otherwise, returns a 404 error
    """

    # Attempt to find a angular in the database based on the provided ID
    cursor = db.process.angular.find_one({'_id': _id})

    # If no angular is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'angular by ID: ({_id}) does not exist')
    else:

        # If the angular is found, convert the cursor data into a angular object and return it
        return Angular(**cursor)


# This route gets a limited amount of angular
@router.get('/limited/', operation_id='get_limited_angular')
async def get_limited_angular(limit: int = 4) -> list[Angular]:
    """
    Handles the retrieval of a limited amount of angular from the database.

    :param limit: The maximum number of angular to retrieve (default is 2).
    :return: A list of angular objects containing information about the limited angular.
    """

    # Retrieve a limited number of angular from the database using the limit method
    cursor = db.process.angular.find().limit(limit)

    # Create a list of Angular objects by unpacking data from each document retrieved
    angular_limited_list = [Angular(**document) for document in cursor]

    # Return the list of Angular objects
    return angular_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the angular from the database
@router.get('/admin/', operation_id='get_all_angular_private')
async def get_all_angular_private(current_user: User = Depends(get_current_user)) -> list[Angular]:
    """
    This route handles the retrieval of all the angular from the database

    :return: a list of Angular objects
    """

    # Retrieve all angular from the database using the find method
    cursor = db.process.angular.find()

    # Create a list of Angular objects by unpacking data from each document retrieved
    angular_list = [Angular(**document) for document in cursor]

    # Return the list of Angular objects
    return angular_list


# This route get one Angular by its ID
@router.get('/admin/{_id}', operation_id='get_angular_by_id_private')
async def get_angular_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Angular:
    """
    This route handles the retrieval of one Angular by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the Angular to be retrieved
    :return: If the Angular is found, returns the Angular data; otherwise, returns a 404 error
    """

    # Attempt to find a Angular in the database based on the provided ID
    cursor = db.process.angular.find_one({'_id': _id})

    # If no Angular is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Angular by ID: ({_id}) does not exist')
    else:
        # If the Angular is found, convert the cursor data into a Angular object and return it
        return Angular(**cursor)


# This route adds a new Angular
@router.post('/', operation_id='add_new_angular_private')
async def add_new_Angular(angular: Angular, current_user: User = Depends(get_current_user)) -> Angular | None:
    """
    Handles the addition of a new Angular to the database.

    :param angular: The Angular object representing the new Angular to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Angular object; otherwise, returns None.
    """

    # Convert the Angular object to a dictionary for database insertion
    angular_dict = angular.dict(by_alias=True)

    # Insert the Angular data into the database
    insert_result = db.process.angular.insert_one(angular_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        angular_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Angular object, using the updated dictionary
        return Angular(**angular_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a Angular by its ID
@router.put('/{_id}', operation_id='edit_angular_by_id_private')
async def edit_angular_by_id_private(_id: str, angular: Angular, current_user: User = Depends(get_current_user)) -> Angular | None:
    """
    Handles the editing of a Angular by its ID in the database.

    :param _id: The ID of the Angular to be edited.
    :param angular: The updated Angular object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Angular is successfully edited, returns the updated Angular object; otherwise, returns None.
    """

    # Convert the Angular object to a dictionary
    angular_dict = angular.dict(by_alias=True)

    # Delete the '_id' field from the Angular dictionary to avoid updating the ID
    del angular_dict['_id']

    # Update the Angular in the database using the update_one method
    cursor = db.process.angular.update_one({'_id': _id}, {'$set': angular_dict})

    # Check if the Angular was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated Angular from the database
        updated_document = db.process.angular.find_one({'_id': _id})

        # Check if the updated Angular exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Angular(**updated_document)

    # Return None if the Angular was not updated
    return None


# Delete a Angular by its ID from the database
@router.delete('/{_id}', operation_id='delete_angular_by_id_private')
async def delete_angular_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Handles the deletion of a Angular by its ID from the database.

    :param _id: The ID of the Angular to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the Angular is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the Angular from the database using the delete_one method
    delete_result = db.process.angular.delete_one({'_id': _id})

    # Check if the Angular was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Angular deleted successfully!'}
    else:
        # If the Angular was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Angular by ID: ({_id}) not found!')



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
async def get_angular_image(filename: str):
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
async def upload_angular_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
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
async def list_angular_images(current_user: User = Depends(get_current_user)):
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
async def delete_angular_image(filename: str, current_user: User = Depends(get_current_user)):
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
