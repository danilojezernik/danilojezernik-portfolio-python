"""
Routes Overview:
1. GET / - Retrieve all projects from the database.
2. GET /{_id} - Retrieve a specific project by its ID from the database.
3. DELETE /{_id} - Delete a specific project by its ID from the database.
4. POST / - Add a new project to the database.
5. PUT /{_id} - Edit an existing project by its ID in the database.
"""
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.projects import Projects
from src.domain.user import User
from src.services import db

from src.services.security import get_current_user, require_role

# Define the root media directory and the subdirectory for media files
projects_root_directory = 'media'  # The root directory where all media files are stored
media_directory = os.path.join(projects_root_directory,
                                        'projects_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all projects public
@router.get('/', operation_id='get_all_projects_public')
async def get_all_projects_public():
    """
    This route handles the retrieval of all the projects from the database

    :return: a list of Projects objects containing all the projects in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/{_id}', operation_id='get_projects_by_id_public')
async def get_projects_by_id_public(_id: str) -> Projects:
    """
    This route handles the retrieval of one project by its ID from the database

    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all projects private
@router.get('/admin/', operation_id='get_all_projects_private')
async def get_all_projects_private(current_user: User = Depends(require_role('admin'))):
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects containing all the blogs in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/admin/{_id}', operation_id='get_projects_by_id_private')
async def get_projects_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))):
    """
    This route handles the retrieval of one project by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)


# Add new project
@router.post('/', operation_id='add_new_project_private')
async def add_new_project_private(project: Projects,
                                  current_user: User = Depends(require_role('admin'))) -> Projects | None:
    """
    Handles the addition of a new project to the database.

    :param project: The Projects object representing the new project to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Projects object; otherwise, returns None.
    """

    # Convert the Projects object to a dictionary
    project_dict = project.dict(by_alias=True)

    # Insert the project data into the database
    insert_result = db.process.projects.insert_one(project_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:

        # Update the dictionary with the newly assigned _id
        project_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Projects object
        return Projects(**project_dict)
    else:

        # If the insertion was not acknowledged, return None
        return None


# Edit project by ID
@router.put('/{_id}', operation_id='edit_project_by_id_private')
async def edit_project_by_id_private(_id: str, project: Projects,
                                     current_user: User = Depends(require_role('admin'))) -> Projects | None:
    """
    Handles the editing of a project by its ID in the database.

    :param _id: The ID of the project to be edited.
    :param project: The updated Projects object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the project is successfully edited, returns the updated Projects object; otherwise, returns None.
    """

    # Convert the Projects object to a dictionary
    project_dict = project.dict(by_alias=True)

    # Delete the '_id' field from the project dictionary to avoid updating the ID
    del project_dict['_id']

    # Update the project in the database using the update_one method
    cursor = db.process.projects.update_one({'_id': _id}, {'$set': project_dict})

    # Check if the project was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated project from the database
        updated_document = db.process.projects.find_one({'_id': _id})

        # Check if the updated project exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Projects(**updated_document)

    else:

        # Return None if the project was not updated
        return None


# Delete project by ID
@router.delete('/{_id}', operation_id='delete_project_by_id_private')
async def delete_project_by_id_private(_id: str):
    delete_result = db.process.projects.delete_one({'_id': _id})

    if delete_result.deleted_count > 0:
        return {'message': 'Project deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')


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
async def get_project_image(filename: str):
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
async def upload_project_file(file: UploadFile = File(...), current_user: User = Depends(require_role('admin'))):
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
async def list_project_images(current_user: User = Depends(require_role('admin'))):
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
async def delete_project_image(filename: str, current_user: User = Depends(require_role('admin'))):
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
