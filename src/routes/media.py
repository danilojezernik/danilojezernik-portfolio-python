import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse

from src.domain.user import User
from src.services.security import get_current_user, require_role

# Define the root media directory and the subdirectory for media files
media_root_directory = 'media'  # The root directory where all media files are stored
about_me_media_directory = os.path.join(media_root_directory, 'about_me_media')  # Subdirectory for specific media files

router = APIRouter()  # Create a new APIRouter instance for defining routes


@router.post("/")
async def upload_media_file(file: UploadFile = File(...), current_user: User = Depends(require_role('admin'))):
    """
    Upload a media file to the server and save it to the 'about_me_media' directory.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        # Ensure the upload directory exists, creating it if necessary
        os.makedirs(about_me_media_directory, exist_ok=True)

        # Read the contents of the uploaded file
        contents = await file.read()

        # Define the file name and path where the file will be saved
        file_name = file.filename if file.filename else 'uploaded_file'
        file_path = os.path.join(about_me_media_directory, file_name)

        # Write the file contents to the specified path
        with open(file_path, 'wb') as f:
            f.write(contents)

    except Exception as e:
        # Raise an HTTP 500 error if there was an issue uploading the file
        raise HTTPException(status_code=500, detail=f'There was an error uploading the file: {str(e)}')

    finally:
        # Ensure the file is closed after the operation
        await file.close()

    # Return a success message indicating the file was uploaded successfully
    return {"message": f"Successfully uploaded {file_name} to {about_me_media_directory}"}


@router.get('/{filename}')
async def get_media_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(about_me_media_directory, filename)

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


@router.get('/images/')
async def list_images():
    """
    List all media files in the 'about_me_media' directory.

    :return: A list of filenames in the directory.
    """
    # Check if the upload directory exists
    if not os.path.exists(about_me_media_directory):
        # Raise a 404 error if the directory is not found
        raise HTTPException(status_code=404, detail='Upload directory not found!')

    # List all files in the directory
    image_names = [f for f in os.listdir(about_me_media_directory) if
                   os.path.isfile(os.path.join(about_me_media_directory, f))]

    # Return the list of filenames
    return {"images": image_names}


@router.delete("/{filename}")
async def delete_image(filename: str, current_user: User = Depends(require_role('admin'))):
    """
    Delete a media file from the 'about_me_media' directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    # Define the path to the file to be deleted
    file_path = os.path.join(about_me_media_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Raise a 404 error if the file is not found
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        # Attempt to delete the file
        os.remove(file_path)
    except Exception as e:
        # Raise an HTTP 500 error if there was an issue deleting the file
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")

    # Return a success message indicating the file has been deleted
    return {"message": f"Successfully deleted {filename} from {about_me_media_directory}"}
