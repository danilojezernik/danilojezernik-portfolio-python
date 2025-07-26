"""
TypeScript Routes:

Public Routes:
1. GET all typescript - Retrieve all TypeScript records from the database.
2. GET TypeScript by ID - Retrieve a specific TypeScript record by its ID.
3. GET limited typescript - Retrieve a limited number of TypeScript records.

Private Routes (Require authentication):
4. GET all typescript (private) - Retrieve all TypeScript records for authenticated users.
5. GET TypeScript by ID (private) - Retrieve a specific TypeScript record by its ID for authenticated users.
6. ADD a new TypeScript - Add a new TypeScript record to the database.
7. EDIT a TypeScript by ID - Edit an existing TypeScript record by its ID.
8. DELETE a TypeScript by ID - Delete a TypeScript record by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.domain.article import Article
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_typescript_public')
async def get_all_typescript_public() -> list[Article]:
    """
    Retrieve all TypeScript records from the database.
    """
    return all_data('typescript_articles', Article)


@router.get('/{_id}', operation_id='get_typescript_by_id_public')
async def get_typescript_by_id_public(_id: str) -> Article:
    """
    Retrieve a specific TypeScript record by its ID from the database.
    """
    return data_by_id('typescript_articles', Article, _id)


@router.get('/limited/', operation_id='get_limited_typescript')
async def get_limited_typescript(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of TypeScript records from the database.
    """
    return limited_data('typescript_articles', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_typescript_private')
async def get_all_typescript_private(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all TypeScript records from the database for authenticated users.
    """
    return all_data('typescript_articles', Article)


@router.get('/admin/{_id}', operation_id='get_typescript_by_id_private')
async def get_typescript_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific TypeScript record by its ID for authenticated users.
    """
    return data_by_id('typescript_articles', Article, _id)


@router.post('/', operation_id='add_new_typescript_private')
async def add_new_typescript_private(typescript: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new TypeScript record to the database for authenticated users.
    """
    return add_data('typescript_articles', typescript, Article)


@router.put('/{_id}', operation_id='edit_typescript_by_id_private')
async def edit_typescript_by_id_private(_id: str, typescript: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing TypeScript record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'typescript_articles', typescript, Article)


@router.delete('/{_id}', operation_id='delete_typescript_by_id_private')
async def delete_typescript_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a TypeScript record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'typescript_articles')
