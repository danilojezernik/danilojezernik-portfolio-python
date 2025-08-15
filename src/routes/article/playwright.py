"""
Playwright Routes:

Public Routes:
1. GET all playwright - Retrieve all Playwright records from the database.
2. GET Playwright by ID - Retrieve a specific Playwright record by its ID.
3. GET limited playwright - Retrieve a limited number of Playwright records.

Private Routes (Require authentication):
4. GET all playwright (private) - Retrieve all Playwright records for authenticated users.
5. GET Playwright by ID (private) - Retrieve a specific Playwright record by its ID for authenticated users.
6. ADD a new Playwright - Add a new Playwright record to the database.
7. EDIT an Playwright by ID - Edit an existing Playwright record by its ID.
8. DELETE an Playwright by ID - Delete an Playwright record by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.user import User
from src.domain.article import Article
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, limited_data, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_playwright_public')
async def get_all_playwright_public_article() -> list[Article]:
    """
    Retrieve all Playwright records from the database.
    """
    return all_data('playwright_articles', Article)


@router.get('/{_id}', operation_id='get_playwright_by_id_public')
async def get_playwright_by_id_public_article(_id: str) -> Article:
    """
    Retrieve a specific Playwright record by its ID from the database.
    """
    return data_by_id('playwright_articles', Article, _id)


@router.get('/limited/', operation_id='get_limited_playwright')
async def get_limited_playwright_article(limit: int = 4) -> list[Article]:
    """
    Retrieve a limited number of Playwright records from the database.
    """
    return limited_data('playwright_articles', Article, limit)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_playwright_private')
async def get_all_playwright_private_article(current_user: User = Depends(get_current_user)) -> list[Article]:
    """
    Retrieve all Playwright records from the database for authenticated users.
    """
    return all_data('playwright_articles', Article)


@router.get('/admin/{_id}', operation_id='get_playwright_by_id_private')
async def get_playwright_by_id_private_article(_id: str, current_user: User = Depends(get_current_user)) -> Article:
    """
    Retrieve a specific Playwright record by its ID for authenticated users.
    """
    return data_by_id('playwright_articles', Article, _id)


@router.post('/', operation_id='add_new_playwright_private')
async def add_new_playwright_private_article(playwright: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Add a new Playwright record to the database for authenticated users.
    """
    return add_data('playwright_articles', playwright, Article)


@router.put('/{_id}', operation_id='edit_playwright_by_id_private')
async def edit_playwright_by_id_private_article(_id: str, playwright: Article, current_user: User = Depends(get_current_user)) -> Article | None:
    """
    Edit an existing Playwright record by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'playwright_articles', playwright, Article)


@router.delete('/{_id}', operation_id='delete_playwright_by_id_private')
async def delete_playwright_by_id_private_article(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an Playwright record by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'playwright_articles')
