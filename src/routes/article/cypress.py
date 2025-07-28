"""
Cypress Routes:

Public Routes:
1. GET all angular - Retrieve all Cypress records from the database.
2. GET Cypress by ID - Retrieve a specific Cypress record by its ID.
3. GET limited angular - Retrieve a limited number of Cypress records.

Private Routes (Require authentication):
4. GET all angular (private) - Retrieve all Cypress records for authenticated users.
5. GET Cypress by ID (private) - Retrieve a specific Cypress record by its ID for authenticated users.
6. ADD a new Cypress - Add a new Cypress record to the database.
7. EDIT an Cypress by ID - Edit an existing Cypress record by its ID.
8. DELETE an Cypress by ID - Delete an Cypress record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.article import Article
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_cypress_public')
async def get_all_cypress_public_article() -> list[Article]:
    """
    Retrieve all Cypress records from the database.
    """
    return all_data('cypress_articles', Article)


@router.get('/{_id}', operation_id='get_cypress_by_id_public')
async def get_cypress_by_id_public_article(_id: str) -> Article:
    """
    Retrieve a specific Cypress record by its ID from the database.
    """
    return data_by_id('cypress_articles', Article, _id)


@router.get('/limited/', operation_id='get_limited_cypress')
async def get_limited_cypress_article(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of Cypress records from the database.
    """
    return limited_data('cypress_articles', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_cypress_private')
async def get_all_cypress_private_article(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all Cypress records from the database for authenticated users.
    """
    return all_data('cypress_articles', Article)


@router.get('/admin/{_id}', operation_id='get_cypress_by_id_private')
async def get_cypress_by_id_private_article(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific Cypress record by its ID for authenticated users.
    """
    return data_by_id('cypress_articles', Article, _id)


@router.post('/', operation_id='add_new_cypress_private')
async def add_new_cypress_private_article(angular: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new Cypress record to the database for authenticated users.
    """
    return add_data('cypress_articles', angular, Article)


@router.put('/{_id}', operation_id='edit_cypress_by_id_private')
async def edit_cypress_by_id_private_article(_id: str, angular: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing Cypress record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'cypress_articles', angular, Article)


@router.delete('/{_id}', operation_id='delete_cypress_by_id_private')
async def delete_cypress_by_id_private_article(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Cypress record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'cypress_articles')
