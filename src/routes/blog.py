"""
This module defines API routes for managing blogs

Routes:
1. GET all blogs
2. GET blog by ID
3. ADD a new blog
4. Edit (PUT) and existing blog by ID
5. DELETE a blog by ID
"""

from fastapi import APIRouter, Depends

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

    :return: a list of Blog objects
    """

    cursor = db.process.blog.find()
    return [Blog(**document) for document in cursor]


"""
THIS ROUTES ARE PRIVATE
"""


@router.get('/admin/', operation_id='get_all_blogs_private')
async def get_all_blogs_private(current_user: str = Depends(get_current_user)) -> list[Blog]:
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects
    """

    cursor = db.process.blog.find()
    return [Blog(**document) for document in cursor]