"""
Pytest Routes:

Public Routes:
1. GET all pytest - Retrieve all Pytest records from the database.
2. GET Pytest by ID - Retrieve a specific Pytest record by its ID.
3. GET limited pytest - Retrieve a limited number of Pytest records.

Private Routes (Require authentication):
4. GET all pytest (private) - Retrieve all Pytest records for authenticated users.
5. GET Pytest by ID (private) - Retrieve a specific Pytest record by its ID for authenticated users.
6. ADD a new Pytest - Add a new Pytest record to the database.
7. EDIT a Pytest by ID - Edit an existing Pytest record by its ID.
8. DELETE a Pytest by ID - Delete a Pytest record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_pytest_public')
async def get_all_pytest_public() -> list[Language]:
    """
    Retrieve all Pytest records from the database.
    """
    return all_data('pytest_qa', Language)


@router.get('/{_id}', operation_id='get_pytest_by_id_public')
async def get_pytest_by_id_public(_id: str):
    """
    Retrieve a specific Pytest record by its ID from the database.
    """
    return data_by_id('pytest_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_pytest')
async def get_limited_pytest(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Pytest records from the database.
    """
    return limited_data('pytest_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_pytest_private')
async def get_all_pytest_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Pytest records from the database for authenticated users.
    """
    return all_data('pytest_qa', Language)


@router.get('/admin/{_id}', operation_id='get_pytest_by_id_private')
async def get_pytest_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Pytest record by its ID for authenticated users.
    """
    return data_by_id('pytest_qa', Language, _id)


@router.post('/', operation_id='add_new_pytest_private')
async def add_new_pytest(pytest: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Pytest record to the database for authenticated users.
    """
    return add_data('pytest_qa', pytest, Language)


@router.put('/{_id}', operation_id='edit_pytest_by_id_private')
async def edit_pytest_by_id_private(_id: str, pytest: Language,
                                  current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Pytest record by its ID for authenticated users.
    """
    return edit_data(_id, 'pytest_qa', pytest, Language)


@router.delete('/{_id}', operation_id='delete_pytest_by_id_private')
async def delete_pytest_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a Pytest record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'pytest_qa')
