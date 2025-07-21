"""
Vue Routes:

Public Routes:
1. GET all vue - Retrieve all Vue records from the database.
2. GET Vue by ID - Retrieve a specific Vue record by its ID.
3. GET limited vue - Retrieve a limited number of Vue records.

Private Routes (Require authentication):
4. GET all vue (private) - Retrieve all Vue records for authenticated users.
5. GET Vue by ID (private) - Retrieve a specific Vue record by its ID for authenticated users.
6. ADD a new Vue - Add a new Vue record to the database.
7. EDIT a Vue by ID - Edit an existing Vue record by its ID.
8. DELETE a Vue by ID - Delete a Vue record by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.domain.user import User
from src.domain.language import Language
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_vue_public')
async def get_all_vue_public() -> list[Language]:
    """
    Retrieve all Vue records from the database.
    """
    return all_data('vue', Language)


@router.get('/{_id}', operation_id='get_vue_by_id_public')
async def get_vue_by_id_public(_id: str) -> Language:
    """
    Retrieve a specific Vue record by its ID from the database.
    """
    return data_by_id('vue', Language, _id)


@router.get('/limited/', operation_id='get_limited_vue')
async def get_limited_vue(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Vue records from the database.
    """
    return limited_data('vue', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_vue_private')
async def get_all_vue_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Vue records from the database for authenticated users.
    """
    return all_data('vue', Language)


@router.get('/admin/{_id}', operation_id='get_vue_by_id_private')
async def get_vue_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Vue record by its ID for authenticated users.
    """
    return data_by_id('vue', Language, _id)


@router.post('/', operation_id='add_new_vue_private')
async def add_new_vue_private(vue: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Vue record to the database for authenticated users.
    """
    return add_data('vue', vue, Language)


@router.put('/{_id}', operation_id='edit_vue_by_id_private')
async def edit_vue_by_id_private(_id: str, vue: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Vue record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'vue', vue, Language)


@router.delete('/{_id}', operation_id='delete_vue_by_id_private')
async def delete_vue_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a Vue record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'vue')
