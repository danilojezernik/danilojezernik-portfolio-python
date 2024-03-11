from fastapi import APIRouter, Depends, HTTPException

from src.domain.projects import Projects
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all projects public
@router.get('/', operation_id='get_all_projects_public')
async def get_all_projects_public():
    """
    This route handles the retrieval of all the projects from the database

    :return: a list of Projects objects containing all the projects in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/{_id}', operation_id='get_projects_by_id_public')
async def get_projects_by_id_public(_id: str) -> Projects:
    """
    This route handles the retrieval of one project by its ID from the database

    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all projects private
@router.get('/admin/', operation_id='get_all_projects_private')
async def get_all_projects_private(current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects containing all the blogs in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/admin/{_id}', operation_id='get_projects_by_id_private')
async def get_projects_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of one project by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)
