"""
This module defines API routes for managing blogs

Routes:
1. GET all blogs
2. GET blog by ID
3. ADD a new blog
4. Edit (PUT) and existing blog by ID
5. DELETE a blog by ID
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.blog import Blog
from src.services import db

from src.services.security import get_current_user

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
        return HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
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
"""


@router.get('/admin/', operation_id='get_all_blogs_private')
async def get_all_blogs_private(current_user: str = Depends(get_current_user)) -> list[Blog]:
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
