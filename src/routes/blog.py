"""
Routes:
1. GET all blogs - Retrieve all blogs from the database.
2. GET blog by ID - Retrieve a specific blog by its ID.
3. GET limited blogs - Retrieve a limited number of blogs.
4. GET all blogs (private) - Retrieve all blogs for authenticated users.
5. GET blog by ID (private) - Retrieve a specific blog by its ID for authenticated users.
6. ADD a new blog - Add a new blog to the database.
7. EDIT a blog by ID - Edit an existing blog by its ID.
8. DELETE a blog by ID - Delete a blog by its ID.
"""
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from src.domain.blog import Blog
from src.domain.user import User
from src.services import db, blog_notification
from src.services.security import get_current_user, require_role
from src.template import blog_notifications

# Define the root media directory and the subdirectory for media files
blogs_root_directory = 'media'  # The root directory where all media files are stored
blogs_media_directory = os.path.join(blogs_root_directory, 'blogs_media')  # Subdirectory for specific media files

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the blogs from the database
@router.get('/', operation_id='get_all_blogs_public')
async def get_all_blogs_public() -> list[Blog]:
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects containing all the blogs in the database
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.blog.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    blog_list = [Blog(**document) for document in cursor]

    # Return the list of Blog objects
    return blog_list


# This route get one blog by its ID
@router.get('/{_id}', operation_id='get_blog_by_id_public')
async def get_blog_by_id_public(_id: str):
    """
    This route handles the retrieval of one blog by its ID from the database

    :param _id: The ID of the blog to be retrieved
    :return: If the blog is found, returns the blog data; otherwise, returns a 404 error
    """

    # Attempt to find a blog in the database based on the provided ID
    cursor = db.process.blog.find_one({'_id': _id})

    # If no blog is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
    else:

        # If the blog is found, convert the cursor data into a Blog object and return it
        return Blog(**cursor)


# This route gets a limited amount of blogs
@router.get('/limited/', operation_id='get_limited_blogs')
async def get_limited_blogs(limit: int = 4) -> list[Blog]:
    """
    Handles the retrieval of a limited amount of blogs from the database.

    :param limit: The maximum number of blogs to retrieve (default is 2).
    :return: A list of Blog objects containing information about the limited blogs.
    """

    # Retrieve a limited number of blogs from the database using the limit method
    cursor = db.process.blog.find().limit(limit)

    # Create a list of Blog objects by unpacking data from each document retrieved
    blog_limited_list = [Blog(**document) for document in cursor]

    # Return the list of Blog objects
    return blog_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the blogs from the database
@router.get('/admin/', operation_id='get_all_blogs_private')
async def get_all_blogs_private(current_user: str = Depends(require_role('admin'))) -> list[Blog]:
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.blog.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    blog_list = [Blog(**document) for document in cursor]

    # Return the list of Blog objects
    return blog_list


# This route get one blog by its ID
@router.get('/admin/{_id}', operation_id='get_blog_by_id_private')
async def get_blog_by_id_private(_id: str,  current_user: User = Depends(require_role('admin'))) -> Blog:
    """
    This route handles the retrieval of one blog by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the blog to be retrieved
    :return: If the blog is found, returns the blog data; otherwise, returns a 404 error
    """

    # Attempt to find a blog in the database based on the provided ID
    cursor = db.process.blog.find_one({'_id': _id})

    # If no blog is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
    else:
        # If the blog is found, convert the cursor data into a Blog object and return it
        return Blog(**cursor)


# This route adds a new blog
@router.post('/', operation_id='add_new_blog_private')
async def add_new_blog(blog: Blog, current_user: User = Depends(require_role('admin'))) -> Blog | None:
    """
    Handles the addition of a new blog to the database.

    :param blog: The Blog object representing the new blog to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Blog object; otherwise, returns None.
    """

    # Convert the Blog object to a dictionary for database insertion
    blog_dict = blog.dict(by_alias=True)

    # Insert the blog data into the database
    insert_result = db.process.blog.insert_one(blog_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        blog_dict['_id'] = str(insert_result.inserted_id)

        # Generate the body content for the blog notification email
        body = blog_notifications.html(title=blog.title)

        # Send notification to users that have blog_notification set to true
        if not blog_notification.blog_notification(subject='Nov blog na strani DaniloJezernik.com', body=body):
            # If email notification fails, return None to indicate failure
            return None

        # Return the newly added Blog object, using the updated dictionary
        return Blog(**blog_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a blog by its ID
@router.put('/{_id}', operation_id='edit_blog_by_id_private')
async def edit_blog_by_id_private(_id: str, blog: Blog,  current_user: User = Depends(require_role('admin'))) -> Blog | None:
    """
    Handles the editing of a blog by its ID in the database.

    :param _id: The ID of the blog to be edited.
    :param blog: The updated Blog object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the blog is successfully edited, returns the updated Blog object; otherwise, returns None.
    """

    # Convert the Blog object to a dictionary
    blog_dict = blog.dict(by_alias=True)

    # Delete the '_id' field from the blog dictionary to avoid updating the ID
    del blog_dict['_id']

    # Update the blog in the database using the update_one method
    cursor = db.process.blog.update_one({'_id': _id}, {'$set': blog_dict})

    # Check if the blog was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated blog from the database
        updated_document = db.process.blog.find_one({'_id': _id})

        # Check if the updated blog exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Blog(**updated_document)

    # Return None if the blog was not updated
    return None


# Delete a blog by its ID from the database
@router.delete('/{_id}', operation_id='delete_blog_by_id_private')
async def delete_blog_by_id_private(_id: str,  current_user: User = Depends(require_role('admin'))):
    """
    Handles the deletion of a blog by its ID from the database.

    :param _id: The ID of the blog to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the blog is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the blog from the database using the delete_one method
    delete_result = db.process.blog.delete_one({'_id': _id})

    # Check if the blog was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Blog deleted successfully!'}
    else:
        # If the blog was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) not found!')


"""
Media Routes:
1. POST / - Upload a media file.
2. GET /{filename} - Retrieve a media file by filename.
3. GET /images/ - List all media files.
4. DELETE /{filename} - Delete a media file by filename.
"""


# Upload a media file
@router.post("/media/")
async def upload_blog_file(file: UploadFile = File(...),  current_user: User = Depends(require_role('admin'))):
    """
    Upload a media file to the server.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        upload_directory = blogs_media_directory
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


# Retrieve a media file by filename
@router.get('/media/{filename}')
async def get_blog_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(blogs_media_directory, filename)

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


# List all media files
@router.get('/images/')
async def list_blog_images(current_user: User = Depends(require_role('admin'))):
    """
    List all media files in the upload directory.

    :return: A list of filenames in the upload directory.
    """
    upload_directory = blogs_media_directory
    if not os.path.exists(upload_directory):
        raise HTTPException(status_code=404, detail='Upload directory not found!')
    image_names = [f for f in os.listdir(upload_directory) if os.path.isfile(os.path.join(upload_directory, f))]
    return {"images": image_names}


# Delete a media file by filename
@router.delete("/media/{filename}")
async def delete_blog_image(filename: str,  current_user: User = Depends(require_role('admin'))):
    """
    Delete a media file from the upload directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    upload_directory = blogs_media_directory
    file_path = os.path.join(upload_directory, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")
    return {"message": f"Successfully deleted {filename} from {upload_directory}"}
