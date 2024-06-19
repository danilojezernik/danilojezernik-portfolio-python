# Import necessary modules and libraries
import httpx  # Library for making HTTP requests
from fastapi import APIRouter  # Importing APIRouter from FastAPI framework

# Importing environment variables from src folder
from src import env

# Creating an instance of APIRouter
router = APIRouter()


# Route handler to fetch GitHub repositories
@router.get('/')
async def get_repo():
    """
    Route handler to fetch GitHub repositories of a specific user.

    Returns:
        dict: A dictionary containing the fetched repositories.
    """
    # Constructing the URL to fetch user repositories from GitHub API
    url = f"https://api.github.com/users/{env.GITHUB}/repos"

    # Making an asynchronous HTTP GET request to GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # Getting response from GitHub API
        repos = response.json()  # Parsing JSON response into Python dictionary

    # Returning the fetched repositories as a dictionary
    return {'repos': repos}
