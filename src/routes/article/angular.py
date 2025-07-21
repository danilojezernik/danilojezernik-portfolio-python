"""
Angular Routes:

Public Routes:
1. GET all angular - Retrieve all Angular records from the database.
2. GET Angular by ID - Retrieve a specific Angular record by its ID.
3. GET limited angular - Retrieve a limited number of Angular records.

Private Routes (Require authentication):
4. GET all angular (private) - Retrieve all Angular records for authenticated users.
5. GET Angular by ID (private) - Retrieve a specific Angular record by its ID for authenticated users.
6. ADD a new Angular - Add a new Angular record to the database.
7. EDIT an Angular by ID - Edit an existing Angular record by its ID.
8. DELETE an Angular by ID - Delete an Angular record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.article import Article
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_angular_public')
async def get_all_angular_public() -> list[Article]:
    """
    Retrieve all Angular records from the database.
    """
    return all_data('angular', Article)


@router.get('/{_id}', operation_id='get_angular_by_id_public')
async def get_angular_by_id_public(_id: str) -> Article:
    """
    Retrieve a specific Angular record by its ID from the database.
    """
    return data_by_id('angular', Article, _id)


@router.get('/limited/', operation_id='get_limited_angular')
async def get_limited_angular(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of Angular records from the database.
    """
    return limited_data('angular', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_angular_private')
async def get_all_angular_private(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all Angular records from the database for authenticated users.
    """
    return all_data('angular', Article)


@router.get('/admin/{_id}', operation_id='get_angular_by_id_private')
async def get_angular_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific Angular record by its ID for authenticated users.
    """
    return data_by_id('angular', Article, _id)


@router.post('/', operation_id='add_new_angular_private')
async def add_new_angular_private(angular: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new Angular record to the database for authenticated users.
    """
    return add_data('angular', angular, Article)


@router.put('/{_id}', operation_id='edit_angular_by_id_private')
async def edit_angular_by_id_private(_id: str, angular: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing Angular record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'angular', angular, Article)


@router.delete('/{_id}', operation_id='delete_angular_by_id_private')
async def delete_angular_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Angular record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'angular')
