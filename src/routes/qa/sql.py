"""
Sql Routes:

Public Routes:
1. GET all sql - Retrieve all sql from the database.
2. GET Sql by ID - Retrieve a specific Sql by its ID.
3. GET limited sql - Retrieve a limited number of sql.

Private Routes (Require authentication):
4. GET all sql (private) - Retrieve all sql for authenticated users.
5. GET Sql by ID (private) - Retrieve a specific Sql by its ID for authenticated users.
6. ADD a new Sql - Add a new Sql to the database.
7. EDIT a Sql by ID - Edit an existing Sql by its ID.
8. DELETE a Sql by ID - Delete a Sql by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.domain.language import Language
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_sql_public')
async def get_all_sql_public() -> list[Language]:
    """
    Retrieve all sql records from the database.
    """
    return all_data('sql_qa', Language)


@router.get('/{_id}', operation_id='get_sql_by_id_public')
async def get_sql_by_id_public(_id: str) -> Language:
    """
    Retrieve a specific sql record by its ID from the database.
    """
    return data_by_id('sql_qa', Language, _id)


@router.get('/limited/', operation_id='get_limited_sql')
async def get_limited_sql(limit: int = 4) -> list[Language]:
    """
    Retrieve a limited number of sql records from the database.
    """
    return limited_data('sql_qa', Language, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_sql_private')
async def get_all_sql_private(current_user: User = Depends(get_current_user)) -> list[Language]:
    """
    Retrieve all sql records from the database for authenticated users.
    """
    return all_data('sql_qa', Language)


@router.get('/admin/{_id}', operation_id='get_sql_by_id_private')
async def get_sql_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Language:
    """
    Retrieve a specific sql record by its ID for authenticated users.
    """
    return data_by_id('sql_qa', Language, _id)


@router.post('/', operation_id='add_new_sql_private')
async def add_new_sql_private(sql: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Add a new sql record to the database for authenticated users.
    """
    return add_data('sql_qa', sql, Language)


@router.put('/{_id}', operation_id='edit_sql_by_id_private')
async def edit_sql_by_id_private(_id: str, sql: Language, current_user: User = Depends(get_current_user)) -> Language | None:
    """
    Edit an existing sql record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'sql_qa', sql, Language)


@router.delete('/{_id}', operation_id='delete_sql_by_id_private')
async def delete_sql_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a sql record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'sql_qa')
