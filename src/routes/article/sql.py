"""
Sql Routes:

Public Routes:
1. GET all sql - Retrieve all Sql records from the database.
2. GET Sql by ID - Retrieve a specific Sql record by its ID.
3. GET limited sql - Retrieve a limited number of Sql records.

Private Routes (Require authentication):
4. GET all sql (private) - Retrieve all Sql records for authenticated users.
5. GET Sql by ID (private) - Retrieve a specific Sql record by its ID for authenticated users.
6. ADD a new Sql - Add a new Sql record to the database.
7. EDIT a Sql by ID - Edit an existing Sql record by its ID.
8. DELETE a Sql by ID - Delete a Sql record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.article import Article
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_sql_public')
async def get_all_sql_public() -> list[Article]:
    """
    Retrieve all Sql records from the database.
    """
    return all_data('sql_articles', Article)


@router.get('/{_id}', operation_id='get_sql_by_id_public')
async def get_sql_by_id_public(_id: str):
    """
    Retrieve a specific Sql record by its ID from the database.
    """
    return data_by_id('sql_articles', Article, _id)


@router.get('/limited/', operation_id='get_limited_sql')
async def get_limited_sql(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of Sql records from the database.
    """
    return limited_data('sql_articles', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_sql_private')
async def get_all_sql_private(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all Sql records from the database for authenticated users.
    """
    return all_data('sql_articles', Article)


@router.get('/admin/{_id}', operation_id='get_sql_by_id_private')
async def get_sql_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific Sql record by its ID for authenticated users.
    """
    return data_by_id('sql_articles', Article, _id)


@router.post('/', operation_id='add_new_sql_private')
async def add_new_sql(sql: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new Sql record to the database for authenticated users.
    """
    return add_data('sql_articles', sql, Article)


@router.put('/{_id}', operation_id='edit_sql_by_id_private')
async def edit_sql_by_id_private(_id: str, sql: Article,
                                    current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing Sql record by its ID for authenticated users.
    """
    return edit_data(_id, 'sql_articles', sql, Article)


@router.delete('/{_id}', operation_id='delete_sql_by_id_private')
async def delete_sql_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a Sql record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'sql_articles')
