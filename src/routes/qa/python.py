"""
Python Routes:

Public Routes:
1. GET all python - Retrieve all python from the database.
2. GET Python by ID - Retrieve a specific Python by its ID.
3. GET limited python - Retrieve a limited number of python.

Private Routes (Require authentication):
4. GET all python (private) - Retrieve all python for authenticated users.
5. GET Python by ID (private) - Retrieve a specific Python by its ID for authenticated users.
6. ADD a new Python - Add a new Python to the database.
7. EDIT a Python by ID - Edit an existing Python by its ID.
8. DELETE a Python by ID - Delete a Python by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_python_public')
async def get_all_python_public() -> list[Language]:
    """
    Retrieve all python records from the database.
    """
    return all_data('python', Language)


@router.get('/{_id}', operation_id='get_python_by_id_public')
async def get_python_by_id_public(_id: str) -> Language:
    """
    Retrieve a specific python record by its ID from the database.
    """
    return data_by_id('python', Language, _id)


@router.get('/limited/', operation_id='get_limited_python')
async def get_limited_python(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of python records from the database.
    """
    return limited_data('python', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_python_private')
async def get_all_python_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all python records from the database for authenticated users.
    """
    return all_data('python', Language)


@router.get('/admin/{_id}', operation_id='get_python_by_id_private')
async def get_python_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific python record by its ID for authenticated users.
    """
    return data_by_id('python', Language, _id)


@router.post('/', operation_id='add_new_python_private')
async def add_new_python_private(python: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new python record to the database for authenticated users.
    """
    return add_data('python', python, Language)


@router.put('/{_id}', operation_id='edit_python_by_id_private')
async def edit_python_by_id_private(_id: str, python: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing python record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'python', python, Language)


@router.delete('/{_id}', operation_id='delete_python_by_id_private')
async def delete_python_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a python record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'python')
