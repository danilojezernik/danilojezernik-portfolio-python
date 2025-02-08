"""
Blog Routes:

Public Routes:
1. GET all blogs - Retrieve all blogs from the database.
2. GET blog by ID - Retrieve a specific blog by its ID.
3. GET limited blogs - Retrieve a limited number of blogs.

Private Routes (Require authentication):
4. GET all blogs (private) - Retrieve all blogs for authenticated users.
5. GET blog by ID (private) - Retrieve a specific blog by its ID for authenticated users.
6. ADD a new blog - Add a new blog to the database.
7. EDIT a blog by ID - Edit an existing blog by its ID.
8. DELETE a blog by ID - Delete a blog by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.blog import Blog
from src.domain.user import User
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data
from src.services.security import get_current_user

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_blogs_public')
async def get_all_blogs_public():
    """
    Retrieves all blogs from the database.
    """
    return all_data('blog', Blog)

@router.get('/{_id}', operation_id='get_blog_by_id_public')
async def get_blog_by_id_public(_id: str):
    """
    Retrieves a specific blog by its ID from the database.
    """
    return data_by_id('blog', Blog, _id)

@router.get('/limited/', operation_id='get_limited_blogs')
async def get_limited_blogs(limit: int = 4) -> list[Blog]:
    """
    Retrieves a limited number of blogs from the database.
    """
    return limited_data('blog', Blog, limit)

# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_blogs_private')
async def get_all_blogs_private(current_user: str = Depends(get_current_user)) -> list[Blog]:
    """
    Retrieves all blogs from the database for authenticated users.
    """
    return all_data('blog', Blog)

@router.get('/admin/{_id}', operation_id='get_blog_by_id_private')
async def get_blog_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Blog:
    """
    Retrieves a specific blog by its ID for authenticated users.
    """
    return data_by_id('blog', Blog, _id)

@router.post('/', operation_id='add_new_blog_private')
async def add_new_blog(blog: Blog, current_user: User = Depends(get_current_user)) -> Blog | None:
    """
    Adds a new blog to the database for authenticated users.
    """
    return add_data('blog', blog, Blog)

@router.put('/{_id}', operation_id='edit_blog_by_id_private')
async def edit_blog_by_id_private(_id: str, blog: Blog, current_user: User = Depends(get_current_user)) -> Blog | None:
    """
    Edits an existing blog identified by its ID for authenticated users.
    """
    return edit_data(_id, 'blog', blog, Blog)

@router.delete('/{_id}', operation_id='delete_blog_by_id_private')
async def delete_blog_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Deletes a blog identified by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'blog')
