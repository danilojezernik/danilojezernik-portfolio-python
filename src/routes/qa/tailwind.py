"""
Tailwind Routes:

Public Routes:
1. GET all tailwind - Retrieve all Tailwind records from the database.
2. GET Tailwind by ID - Retrieve a specific Tailwind record by its ID.
3. GET limited tailwind - Retrieve a limited number of Tailwind records.

Private Routes (Require authentication):
4. GET all tailwind (private) - Retrieve all Tailwind records for authenticated users.
5. GET Tailwind by ID (private) - Retrieve a specific Tailwind record by its ID for authenticated users.
6. ADD a new Tailwind - Add a new Tailwind record to the database.
7. EDIT a Tailwind by ID - Edit an existing Tailwind record by its ID.
8. DELETE a Tailwind by ID - Delete a Tailwind record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_tailwind_public')
async def get_all_tailwind_public() -> list[Language]:
    """
    Retrieve all Tailwind records from the database.
    """
    return all_data('tailwind_qa', Language)


@router.get('/{_id}', operation_id='get_tailwind_by_id_public')
async def get_tailwind_by_id_public(_id: str):
    """
    Retrieve a specific Tailwind record by its ID from the database.
    """
    return data_by_id('tailwind_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_tailwind')
async def get_limited_tailwind(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Tailwind records from the database.
    """
    return limited_data('tailwind_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_tailwind_private')
async def get_all_tailwind_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Tailwind records from the database for authenticated users.
    """
    return all_data('tailwind_qa', Language)


@router.get('/admin/{_id}', operation_id='get_tailwind_by_id_private')
async def get_tailwind_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Tailwind record by its ID for authenticated users.
    """
    return data_by_id('tailwind_qa', Language, _id)


@router.post('/', operation_id='add_new_tailwind_private')
async def add_new_tailwind(tailwind: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Tailwind record to the database for authenticated users.
    """
    return add_data('tailwind_qa', tailwind, Language)


@router.put('/{_id}', operation_id='edit_tailwind_by_id_private')
async def edit_tailwind_by_id_private(_id: str, tailwind: Language,
                                    current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Tailwind record by its ID for authenticated users.
    """
    return edit_data(_id, 'tailwind_qa', tailwind, Language)


@router.delete('/{_id}', operation_id='delete_tailwind_by_id_private')
async def delete_tailwind_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a Tailwind record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'tailwind_qa')
