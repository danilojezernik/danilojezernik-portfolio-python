"""
Projects Routes:

Public Routes:
1. GET all projects - Retrieve all projects from the database.
2. GET project by ID - Retrieve a specific project by its ID from the database.

Private Routes (Require authentication):
3. GET all projects (private) - Retrieve all projects for authenticated users.
4. GET project by ID (private) - Retrieve a specific project by its ID for authenticated users.
5. ADD a new project - Add a new project to the database.
6. EDIT a project by ID - Edit an existing project by its ID in the database.
7. DELETE a project by ID - Delete a project by its ID from the database.
"""

from fastapi import APIRouter, Depends
from src.domain.projects import Projects
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, add_data, edit_data, delete_data

router = APIRouter()


# Public Routes

@router.get('/', operation_id='get_all_projects_public')
async def get_all_projects_public() -> list[Projects]:
    """
    Retrieve all projects from the database.
    """
    return all_data('projects', Projects)


@router.get('/{_id}', operation_id='get_projects_by_id_public')
async def get_projects_by_id_public(_id: str) -> Projects:
    """
    Retrieve a specific project by its ID from the database.
    """
    return data_by_id('projects', Projects, _id)


# Private Routes (Require authentication)

@router.get('/admin/', operation_id='get_all_projects_private')
async def get_all_projects_private(current_user: User = Depends(get_current_user)) -> list[Projects]:
    """
    Retrieve all projects from the database for authenticated users.
    """
    return all_data('projects', Projects)


@router.get('/admin/{_id}', operation_id='get_projects_by_id_private')
async def get_projects_by_id_private(_id: str, current_user: User = Depends(get_current_user)) -> Projects:
    """
    Retrieve a specific project by its ID for authenticated users.
    """
    return data_by_id('projects', Projects, _id)


@router.post('/', operation_id='add_new_project_private')
async def add_new_project_private(project: Projects, current_user: User = Depends(get_current_user)) -> Projects | None:
    """
    Add a new project to the database for authenticated users.
    """
    return add_data('projects', project, Projects)


@router.put('/{_id}', operation_id='edit_project_by_id_private')
async def edit_project_by_id_private(_id: str, project: Projects,
                                     current_user: User = Depends(get_current_user)) -> Projects | None:
    """
    Edit an existing project by its ID in the database for authenticated users.
    """
    return edit_data(_id, 'projects', project, Projects)


@router.delete('/{_id}', operation_id='delete_project_by_id_private')
async def delete_project_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a project by its ID from the database for authenticated users.
    """
    return delete_data(_id, 'projects')
