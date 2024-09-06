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
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.python import Python
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user, require_role

# Define the root media directory and the subdirectory for media files
python_root_directory = 'media'  # The root directory where all media files are stored
python_media_directory = os.path.join(python_root_directory, 'python_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the python from the database
@router.get('/', operation_id='get_all_python_public')
async def get_all_python_public() -> list[Python]:
    """
    This route handles the retrieval of all the python from the database

    :return: a list of Python objects containing all the python in the database
    """

    # Retrieve all python from the database using the find method
    cursor = db.process.python.find()

    # Create a list of Python objects by unpacking data from each document retrieved
    python_list = [Python(**document) for document in cursor]

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
        return Python(**cursor)


# This route gets a limited amount of python
@router.get('/limited/', operation_id='get_limited_python')
async def get_limited_python(limit: int = 4) -> list[Python]:
    """
    Handles the retrieval of a limited amount of python from the database.

    :param limit: The maximum number of python to retrieve (default is 2).
    :return: A list of python objects containing information about the limited python.
    """

    # Retrieve a limited number of python from the database using the limit method
    cursor = db.process.python.find().limit(limit)

    # Create a list of Python objects by unpacking data from each document retrieved
    python_limited_list = [Python(**document) for document in cursor]

    # Return the list of Python objects
    return python_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the python from the database
@router.get('/admin/', operation_id='get_all_python_private')
async def get_all_python_private(current_user: User = Depends(require_role('admin'))) -> list[Python]:
    """
    This route handles the retrieval of all the python from the database

    :return: a list of Python objects
    """

    # Retrieve all python from the database using the find method
    cursor = db.process.python.find()

    # Create a list of Python objects by unpacking data from each document retrieved
    python_list = [Python(**document) for document in cursor]

    # Return the list of Python objects
    return python_list


# This route get one Python by its ID
@router.get('/admin/{_id}', operation_id='get_python_by_id_private')
async def get_python_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))) -> Python:
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
        return Python(**cursor)


# This route adds a new Python
@router.post('/', operation_id='add_new_python_private')
async def add_new_python(python: Python, current_user: User = Depends(require_role('admin'))) -> Python | None:
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
        return Python(**python_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a Python by its ID
@router.put('/{_id}', operation_id='edit_python_by_id_private')
async def edit_python_by_id_private(_id: str, python: Python,
                                    current_user: User = Depends(require_role('admin'))) -> Python | None:
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
            return Python(**updated_document)

    # Return None if the Python was not updated
    return None


# Delete a Python by its ID from the database
@router.delete('/{_id}', operation_id='delete_python_by_id_private')
async def delete_python_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))):
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
async def get_python_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(python_media_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Raise a 404 error if the file is not found
        raise HTTPException(status_code=404, detail='Image not found!')

    try:
        # Return the file as a response
        return FileResponse(file_path)
    except Exception as e:
        # Raise an HTTP 500 error if there was an issue serving the file
        raise HTTPException(status_code=500, detail=f'Error serving file: {str(e)}')


# PRIVATE

# Upload a media file
@router.post("/media/")
async def upload_python_file(file: UploadFile = File(...), current_user: User = Depends(require_role('admin'))):
    """
    Upload a media file to the server.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        upload_directory = python_media_directory
        os.makedirs(upload_directory, exist_ok=True)
        contents = await file.read()
        file_name = file.filename if file.filename else 'uploaded_file'
        file_path = os.path.join(upload_directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'There was an error uploading the file: {str(e)}')
    finally:
        await file.close()
    return {"message": f"Successfully uploaded {file_name} to {upload_directory}"}


# List all media files
@router.get('/images/')
async def list_python_images(current_user: User = Depends(require_role('admin'))):
    """
    List all media files in the upload directory.

    :return: A list of filenames in the upload directory.
    """
    upload_directory = python_media_directory
    if not os.path.exists(upload_directory):
        raise HTTPException(status_code=404, detail='Upload directory not found!')
    image_names = [f for f in os.listdir(upload_directory) if os.path.isfile(os.path.join(upload_directory, f))]
    return {"images": image_names}


# Delete a media file by filename
@router.delete("/media/{filename}")
async def delete_python_image(filename: str, current_user: User = Depends(require_role('admin'))):
    """
    Delete a media file from the upload directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    upload_directory = python_media_directory
    file_path = os.path.join(upload_directory, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")
    return {"message": f"Successfully deleted {filename} from {upload_directory}"}
