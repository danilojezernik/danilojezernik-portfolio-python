"""
MongoDb Routes:

Public Routes:
1. GET all mongodb - Retrieve all MongoDb records from the database.
2. GET MongoDb by ID - Retrieve a specific MongoDb record by its ID.
3. GET limited mongodb - Retrieve a limited number of MongoDb records.

Private Routes (Require authentication):
4. GET all mongodb (private) - Retrieve all MongoDb records for authenticated users.
5. GET MongoDb by ID (private) - Retrieve a specific MongoDb record by its ID for authenticated users.
6. ADD a new MongoDb - Add a new MongoDb record to the database.
7. EDIT a MongoDb by ID - Edit an existing MongoDb record by its ID.
8. DELETE a MongoDb by ID - Delete a MongoDb record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_mongodb_public')
async def get_all_mongodb_public() -> list[Language]:
    """
    Retrieve all MongoDb records from the database.
    """
    return all_data('mongodb_qa', Language)


@router.get('/{_id}', operation_id='get_mongodb_by_id_public')
async def get_mongodb_by_id_public(_id: str):
    """
    Retrieve a specific MongoDb record by its ID from the database.
    """
    return data_by_id('mongodb_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_mongodb')
async def get_limited_mongodb(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of MongoDb records from the database.
    """
    return limited_data('mongodb_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_mongodb_private')
async def get_all_mongodb_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all MongoDb records from the database for authenticated users.
    """
    return all_data('mongodb_qa', Language)


@router.get('/admin/{_id}', operation_id='get_mongodb_by_id_private')
async def get_mongodb_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific MongoDb record by its ID for authenticated users.
    """
    return data_by_id('mongodb_qa', Language, _id)


@router.post('/', operation_id='add_new_mongodb_private')
async def add_new_mongodb(mongodb: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new MongoDb record to the database for authenticated users.
    """
    return add_data('mongodb_qa', mongodb, Language)


@router.put('/{_id}', operation_id='edit_mongodb_by_id_private')
async def edit_mongodb_by_id_private(_id: str, mongodb: Language,
                                     current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing MongoDb record by its ID for authenticated users.
    """
    return edit_data(_id, 'mongodb_qa', mongodb, Language)


@router.delete('/{_id}', operation_id='delete_mongodb_by_id_private')
async def delete_mongodb_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a MongoDb record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'mongodb_qa')
