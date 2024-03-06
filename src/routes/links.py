"""
This module defines API routes for managing links

Routes:
1. GET all links
2. GET links by ID
3. ADD a new links
4. Edit (PUT) and existing links by ID
5. DELETE a links by ID
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.links import Links
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all the links from database
@router.get('/', operation_id='get_all_links_public')
async def get_all_links_public():
    """
    This route handles the retrieval of all the links from the database

    :return: a list of Links objects containing all the links in the database
    """

    # Retrieve all links from the database using the find method
    cursor = db.process.links.find()

    # Create a list of Links objects by unpacking data from each document retrieved
    links_list = [Links(**document) for document in cursor]

    # Return the list of Links objects
    return links_list


"""
THIS ROUTES ARE PRIVATE
"""


@router.get('/admin/', operation_id='get_all_links_private')
async def get_all_links_private(current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of all the links from the database

    :return: a list of Links objects containing all the links in the database
    """

    # Retrieve all links from the database using the find method
    cursor = db.process.links.find()

    # Create a list of Links objects by unpacking data from each document retrieved
    links_list = [Links(**document) for document in cursor]

    # Return the list of Links objects
    return links_list
