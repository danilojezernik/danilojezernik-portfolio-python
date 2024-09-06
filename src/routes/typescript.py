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
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.typescript import TypeScript
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user, require_role

# Define the root media directory and the subdirectory for media files
typescript_root_directory = 'media'  # The root directory where all media files are stored
typescript_media_directory = os.path.join(typescript_root_directory,
                                          'typescript_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the typescript from the database
@router.get('/', operation_id='get_all_typescript_public')
async def get_all_typescript_public() -> list[TypeScript]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of TypeScript objects containing all the typescript in the database
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.typescript.find()

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_list = [TypeScript(**document) for document in cursor]

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
        return TypeScript(**cursor)


# This route gets a limited amount of typescript
@router.get('/limited/', operation_id='get_limited_typescript')
async def get_limited_typescript(limit: int = 4) -> list[TypeScript]:
    """
    Handles the retrieval of a limited amount of typescript from the database.

    :param limit: The maximum number of typescript to retrieve (default is 2).
    :return: A list of typescript objects containing information about the limited typescript.
    """

    # Retrieve a limited number of typescript from the database using the limit method
    cursor = db.process.typescript.find().limit(limit)

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_limited_list = [TypeScript(**document) for document in cursor]

    # Return the list of TypeScript objects
    return typescript_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the typescript from the database
@router.get('/admin/', operation_id='get_all_typescript_private')
async def get_all_typescript_private(current_user: User = Depends(require_role('admin'))) -> list[TypeScript]:
    """
    This route handles the retrieval of all the typescript from the database

    :return: a list of TypeScript objects
    """

    # Retrieve all typescript from the database using the find method
    cursor = db.process.typescript.find()

    # Create a list of TypeScript objects by unpacking data from each document retrieved
    typescript_list = [TypeScript(**document) for document in cursor]

    # Return the list of TypeScript objects
    return typescript_list


# This route get one TypeScript by its ID
@router.get('/admin/{_id}', operation_id='get_typescript_by_id_private')
async def get_typescript_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))) -> TypeScript:
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
        return TypeScript(**cursor)


# This route adds a new TypeScript
@router.post('/', operation_id='add_new_typescript_private')
async def add_new_typescript(typescript: TypeScript,
                             current_user: User = Depends(require_role('admin'))) -> TypeScript | None:
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
        return TypeScript(**typescript_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a TypeScript by its ID
@router.put('/{_id}', operation_id='edit_typescript_by_id_private')
async def edit_typescript_by_id_private(_id: str, typescript: TypeScript,
                                        current_user: User = Depends(require_role('admin'))) -> TypeScript | None:
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
            return TypeScript(**updated_document)

    # Return None if the TypeScript was not updated
    return None


# Delete a TypeScript by its ID from the database
@router.delete('/{_id}', operation_id='delete_typescript_by_id_private')
async def delete_typescript_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))):
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
async def get_typescript_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(typescript_media_directory, filename)

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
async def upload_typescript_file(file: UploadFile = File(...), current_user: User = Depends(require_role('admin'))):
    """
    Upload a media file to the server.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        upload_directory = typescript_media_directory
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
async def list_typescript_images(current_user: User = Depends(require_role('admin'))):
    """
    List all media files in the upload directory.

    :return: A list of filenames in the upload directory.
    """
    upload_directory = typescript_media_directory
    if not os.path.exists(upload_directory):
        raise HTTPException(status_code=404, detail='Upload directory not found!')
    image_names = [f for f in os.listdir(upload_directory) if os.path.isfile(os.path.join(upload_directory, f))]
    return {"images": image_names}


# Delete a media file by filename
@router.delete("/media/{filename}")
async def delete_typescript_image(filename: str, current_user: User = Depends(require_role('admin'))):
    """
    Delete a media file from the upload directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    upload_directory = typescript_media_directory
    file_path = os.path.join(upload_directory, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")
    return {"message": f"Successfully deleted {filename} from {upload_directory}"}
