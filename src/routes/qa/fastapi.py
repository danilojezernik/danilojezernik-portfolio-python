"""
Fastapi Routes:

Public Routes:
1. GET all fastapi - Retrieve all Fastapi records from the database.
2. GET Fastapi by ID - Retrieve a specific Fastapi record by its ID.
3. GET limited fastapi - Retrieve a limited number of Fastapi records.

Private Routes (Require authentication):
4. GET all fastapi (private) - Retrieve all Fastapi records for authenticated users.
5. GET Fastapi by ID (private) - Retrieve a specific Fastapi record by its ID for authenticated users.
6. ADD a new Fastapi - Add a new Fastapi record to the database.
7. EDIT an Fastapi by ID - Edit an existing Fastapi record by its ID.
8. DELETE an Fastapi by ID - Delete an Fastapi record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.language import Language
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_fastapi_public')
async def get_all_fastapi_public_qa() -> list[Language]:
    """
    Retrieve all Fastapi records from the database.
    """
    return all_data('fastapi_qa', Language)


@router.get('/{_id}', operation_id='get_fastapi_by_id_public')
async def get_fastapi_by_id_public_qa(_id: str) -> Language:
    """
    Retrieve a specific fastapi record by its ID from the database.
    """
    return data_by_id('fastapi_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_fastapi')
async def get_limited_fastapi_qa(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Fastapi records from the database.
    """
    return limited_data('fastapi_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_fastapi_private')
async def get_all_fastapi_private_qa(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Fastapi records from the database for authenticated users.
    """
    return all_data('fastapi_qa', Language)


@router.get('/admin/{_id}', operation_id='get_fastapi_by_id_private')
async def get_fastapi_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Fastapi record by its ID for authenticated users.
    """
    return data_by_id('fastapi_qa', Language, _id)


@router.post('/', operation_id='add_new_fastapi_private')
async def add_new_fastapi_private_qa(fastapi: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Fastapi record to the database for authenticated users.
    """
    return add_data('fastapi_qa', fastapi, Language)


@router.put('/{_id}', operation_id='edit_fastapi_by_id_private')
async def edit_fastapi_by_id_private_qa(_id: str, fastapi: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Fastapi record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'fastapi_qa', fastapi, Language)


@router.delete('/{_id}', operation_id='delete_fastapi_by_id_private')
async def delete_fastapi_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Fastapi record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'fastapi_qa')
