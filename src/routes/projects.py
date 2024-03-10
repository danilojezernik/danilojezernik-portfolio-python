from fastapi import APIRouter, Depends, HTTPException

from src.domain.projects import Projects
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


@router.get('/', operation_id='get_all_projects_public')
async def get_all_projects_public():
    cursor = db.process.projects.find()

    projects_lists = [Projects(**document) for document in cursor]

    return projects_lists


"""
THIS ROUTES ARE PRIVATE
"""
