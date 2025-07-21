"""
JavaScript Routes:

Public Routes:
1. GET all javascript - Retrieve all JavaScript records from the database.
2. GET JavaScript by ID - Retrieve a specific JavaScript record by its ID.
3. GET limited javascript - Retrieve a limited number of JavaScript records.

Private Routes (Require authentication):
4. GET all javascript (private) - Retrieve all JavaScript records for authenticated users.
5. GET JavaScript by ID (private) - Retrieve a specific JavaScript record by its ID for authenticated users.
6. ADD a new JavaScript - Add a new JavaScript record to the database.
7. EDIT a JavaScript by ID - Edit an existing JavaScript record by its ID.
8. DELETE a JavaScript by ID - Delete a JavaScript record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.article import Article
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_javascript_public')
async def get_all_javascript_public() -> list[Article]:
    """
    Retrieve all JavaScript records from the database.
    """
    return all_data('javascript', Article)


@router.get('/{_id}', operation_id='get_javascript_by_id_public')
async def get_javascript_by_id_public(_id: str):
    """
    Retrieve a specific JavaScript record by its ID from the database.
    """
    return data_by_id('javascript', Article, _id)


@router.get('/limited/', operation_id='get_limited_javascript')
async def get_limited_javascript(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of JavaScript records from the database.
    """
    return limited_data('javascript', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_javascript_private')
async def get_all_javascript_private(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all JavaScript records from the database for authenticated users.
    """
    return all_data('javascript', Article)


@router.get('/admin/{_id}', operation_id='get_javascript_by_id_private')
async def get_javascript_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific JavaScript record by its ID for authenticated users.
    """
    return data_by_id('javascript', Article, _id)


@router.post('/', operation_id='add_new_javascript_private')
async def add_new_javascript(javascript: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new JavaScript record to the database for authenticated users.
    """
    return add_data('javascript', javascript, Article)


@router.put('/{_id}', operation_id='edit_javascript_by_id_private')
async def edit_javascript_by_id_private(_id: str, javascript: Article,
                                        current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing JavaScript record by its ID for authenticated users.
    """
    return edit_data(_id, 'javascript', javascript, Article)


@router.delete('/{_id}', operation_id='delete_javascript_by_id_private')
async def delete_javascript_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a JavaScript record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'javascript')
