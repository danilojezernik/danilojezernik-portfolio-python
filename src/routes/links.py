"""
Links Routes:

Public Routes:
1. GET all links - Retrieve all links from the database.
2. GET link by ID - Retrieve a specific link by its ID.

Private Routes (Require authentication):
3. GET all links (private) - Retrieve all links for authenticated users.
4. ADD a new link - Add a new link to the database.
5. GET link by ID (private) - Retrieve a specific link by its ID for authenticated users.
6. EDIT link by ID (private) - Edit an existing link by its ID for authenticated users.
7. DELETE link by ID (private) - Delete a link from the database by its ID for authenticated users.
"""

from fastapi import APIRouter, Depends
from src.domain.links import Links
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_links_public')
async def get_all_links_public() -> list[Links]:
    """
    Retrieves all links from the database.
    """
    return all_data('links', Links)


@router.get('/{_id}', operation_id='get_link_by_id')
async def get_link_by_id(_id: str) -> Links:
    """
    Retrieves a specific link by its ID from the database.
    """
    return data_by_id('links', Links, _id)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_links_private')
async def get_all_links_private(current_user: User = Depends(get_current_user)) -> list[Links]:
    """
    Retrieves all links from the database for authenticated users.
    """
    return all_data('links', Links)


@router.post('/', operation_id='add_new_link_private')
async def add_new_link_private(links: Links, current_user: User = Depends(get_current_user)) -> Links | None:
    """
    Adds a new link to the database for authenticated users.
    """
    return add_data('links', links, Links)


@router.put('/{_id}', operation_id='edit_link_private')
async def edit_link_private(_id: str, links: Links, current_user: User = Depends(get_current_user)) -> Links | None:
    """
    Edits an existing link identified by its ID for authenticated users.
    """
    return edit_data(_id, 'links', links, Links)


@router.delete('/{_id}', operation_id='delete_links_by_id_private')
async def delete_links_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Deletes a link identified by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'links')
