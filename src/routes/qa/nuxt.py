"""
Nuxt Routes:

Public Routes:
1. GET all nuxt - Retrieve all Nuxt records from the database.
2. GET Nuxt by ID - Retrieve a specific Nuxt record by its ID.
3. GET limited nuxt - Retrieve a limited number of Nuxt records.

Private Routes (Require authentication):
4. GET all nuxt (private) - Retrieve all Nuxt records for authenticated users.
5. GET Nuxt by ID (private) - Retrieve a specific Nuxt record by its ID for authenticated users.
6. ADD a new Nuxt - Add a new Nuxt record to the database.
7. EDIT a Nuxt by ID - Edit an existing Nuxt record by its ID.
8. DELETE a Nuxt by ID - Delete a Nuxt record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_nuxt_public')
async def get_all_nuxt_public() -> list[Language]:
    """
    Retrieve all Nuxt records from the database.
    """
    return all_data('nuxt_qa', Language)


@router.get('/{_id}', operation_id='get_nuxt_by_id_public')
async def get_nuxt_by_id_public(_id: str):
    """
    Retrieve a specific Nuxt record by its ID from the database.
    """
    return data_by_id('nuxt_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_nuxt')
async def get_limited_nuxt(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Nuxt records from the database.
    """
    return limited_data('nuxt_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_nuxt_private')
async def get_all_nuxt_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Nuxt records from the database for authenticated users.
    """
    return all_data('nuxt_qa', Language)


@router.get('/admin/{_id}', operation_id='get_nuxt_by_id_private')
async def get_nuxt_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Nuxt record by its ID for authenticated users.
    """
    return data_by_id('nuxt_qa', Language, _id)


@router.post('/', operation_id='add_new_nuxt_private')
async def add_new_nuxt(nuxt: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Nuxt record to the database for authenticated users.
    """
    return add_data('nuxt_qa', nuxt, Language)


@router.put('/{_id}', operation_id='edit_nuxt_by_id_private')
async def edit_nuxt_by_id_private(_id: str, nuxt: Language,
                                     current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Nuxt record by its ID for authenticated users.
    """
    return edit_data(_id, 'nuxt_qa', nuxt, Language)


@router.delete('/{_id}', operation_id='delete_nuxt_by_id_private')
async def delete_nuxt_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a Nuxt record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'nuxt_qa')
