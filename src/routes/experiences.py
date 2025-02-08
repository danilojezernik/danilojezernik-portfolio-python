"""
Routes Overview:
1. GET / - Retrieve all experiences from the database (public).
2. GET /{_id} - Retrieve a specific experience by its ID (public).
3. GET /admin/ - Retrieve all experiences from the database (private).
4. POST / - Add a new experience to the database (private).
5. GET /admin/{_id} - Retrieve a specific experience by its ID (private).
6. PUT /{_id} - Update an existing experience by its ID (private).
7. DELETE /{_id} - Delete an experience from the database by its ID (private).
"""

from fastapi import APIRouter, Depends
from src.domain.experiences import Experiences
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_experiences_public')
async def get_all_experiences_public() -> list[Experiences]:
    """
    Retrieve all experiences from the database.
    """
    return all_data('experiences', Experiences)


@router.get('/{_id}', operation_id='get_experiences_by_id_public')
async def get_experiences_by_id_public(_id: str) -> Experiences:
    """
    Retrieve a specific experience by its ID from the database.
    """
    return data_by_id('experiences', Experiences, _id)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_experiences_private')
async def get_all_experiences_private(current_user: User = Depends(get_current_user)) -> list[Experiences]:
    """
    Retrieve all experiences from the database for authenticated users.
    """
    return all_data('experiences', Experiences)


@router.get('/admin/{_id}', operation_id='get_experiences_by_id_private')
async def get_experiences_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Experiences:
    """
    Retrieve a specific experience by its ID for authenticated users.
    """
    return data_by_id('experiences', Experiences, _id)


@router.post('/', operation_id='add_new_experiences_private')
async def add_new_experiences_private(experiences: Experiences, current_user: User = Depends(get_current_user)) -> Experiences | None:
    """
    Add a new experience to the database for authenticated users.
    """
    return add_data('experiences', experiences, Experiences)


@router.put('/{_id}', operation_id='edit_experiences_by_id_private')
async def edit_experiences_by_id_private(_id: str, experiences: Experiences, current_user: User = Depends(get_current_user)) -> Experiences | None:
    """
    Update an existing experience by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'experiences', experiences, Experiences)


@router.delete('/{_id}', operation_id='delete_experiences_by_id_private')
async def delete_experiences_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an experience from the database by its ID for authenticated users.
    """
    return delete_data(_id, 'experiences')
