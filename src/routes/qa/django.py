"""
Django Routes:

Public Routes:
1. GET all angular - Retrieve all Django records from the database.
2. GET Django by ID - Retrieve a specific Django record by its ID.
3. GET limited angular - Retrieve a limited number of Django records.

Private Routes (Require authentication):
4. GET all angular (private) - Retrieve all Django records for authenticated users.
5. GET Django by ID (private) - Retrieve a specific Django record by its ID for authenticated users.
6. ADD a new Django - Add a new Django record to the database.
7. EDIT an Django by ID - Edit an existing Django record by its ID.
8. DELETE an Django by ID - Delete an Django record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.language import Language
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_django_public')
async def get_all_django_public_qa() -> list[Language]:
    """
    Retrieve all Django records from the database.
    """
    return all_data('django_qa', Language)


@router.get('/{_id}', operation_id='get_django_by_id_public')
async def get_django_by_id_public_qa(_id: str) -> Language:
    """
    Retrieve a specific django record by its ID from the database.
    """
    return data_by_id('django_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_django')
async def get_limited_django_qa(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Django records from the database.
    """
    return limited_data('django_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_django_private')
async def get_all_django_private_qa(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Django records from the database for authenticated users.
    """
    return all_data('django_qa', Language)


@router.get('/admin/{_id}', operation_id='get_django_by_id_private')
async def get_django_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Django record by its ID for authenticated users.
    """
    return data_by_id('django_qa', Language, _id)


@router.post('/', operation_id='add_new_django_private')
async def add_new_django_private_qa(angular: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Django record to the database for authenticated users.
    """
    return add_data('django_qa', angular, Language)


@router.put('/{_id}', operation_id='edit_django_by_id_private')
async def edit_django_by_id_private_qa(_id: str, angular: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Django record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'django_qa', angular, Language)


@router.delete('/{_id}', operation_id='delete_django_by_id_private')
async def delete_django_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Django record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'django_qa')
