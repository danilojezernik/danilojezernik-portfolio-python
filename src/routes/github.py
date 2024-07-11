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
    username = env.GITHUB  # Assuming 'env.GITHUB' contains the GitHub username
    per_page = 30  # Number of repositories per page
    total_repos_to_fetch = 44  # Total number of repositories to fetch
    repos = []  # List to store all fetched repositories

    async with httpx.AsyncClient() as client:
        for page in range(1, (total_repos_to_fetch // per_page) + 2):
            url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
            response = await client.get(url)
            page_repos = response.json()

            # Check if the response contains repositories
            if page_repos:
                # Filter public repositories and add them to the list
                public_repos = [repo for repo in page_repos if not repo.get('private')]
                repos.extend(public_repos)

            # Break the loop if we have fetched enough repositories
            if len(repos) >= total_repos_to_fetch:
                break

    # Limit the number of repositories to the desired amount
    repos = repos[:total_repos_to_fetch]

    # Returning the fetched repositories as a dictionary
    return {'repos': repos}
