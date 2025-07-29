"""
Docker Routes:

Public Routes:
1. GET all docker - Retrieve all Docker records from the database.
2. GET Docker by ID - Retrieve a specific Docker record by its ID.
3. GET limited docker - Retrieve a limited number of Docker records.

Private Routes (Require authentication):
4. GET all docker (private) - Retrieve all Docker records for authenticated users.
5. GET Docker by ID (private) - Retrieve a specific Docker record by its ID for authenticated users.
6. ADD a new Docker - Add a new Docker record to the database.
7. EDIT an Docker by ID - Edit an existing Docker record by its ID.
8. DELETE an Docker by ID - Delete an Docker record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.language import Language
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_docker_public')
async def get_all_docker_public_qa() -> list[Language]:
    """
    Retrieve all Docker records from the database.
    """
    return all_data('docker_qa', Language)


@router.get('/{_id}', operation_id='get_docker_by_id_public')
async def get_docker_by_id_public_qa(_id: str) -> Language:
    """
    Retrieve a specific docker record by its ID from the database.
    """
    return data_by_id('docker_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_docker')
async def get_limited_docker_qa(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of Docker records from the database.
    """
    return limited_data('docker_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_docker_private')
async def get_all_docker_private_qa(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all Docker records from the database for authenticated users.
    """
    return all_data('docker_qa', Language)


@router.get('/admin/{_id}', operation_id='get_docker_by_id_private')
async def get_docker_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific Docker record by its ID for authenticated users.
    """
    return data_by_id('docker_qa', Language, _id)


@router.post('/', operation_id='add_new_docker_private')
async def add_new_docker_private_qa(docker: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new Docker record to the database for authenticated users.
    """
    return add_data('docker_qa', docker, Language)


@router.put('/{_id}', operation_id='edit_docker_by_id_private')
async def edit_docker_by_id_private_qa(_id: str, docker: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing Docker record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'docker_qa', docker, Language)


@router.delete('/{_id}', operation_id='delete_docker_by_id_private')
async def delete_docker_by_id_private_qa(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Docker record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'docker_qa')
