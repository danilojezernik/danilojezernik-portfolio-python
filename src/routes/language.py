# Import necessary modules and libraries
from fastapi import APIRouter

import requests

# Creating an instance of APIRouter
router = APIRouter()

# Function to fetch popular tags from Stack Overflow API
def get_stackoverflow_tags():
    url = 'https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow'
    response = requests.get(url)
    data = response.json()

    tags = []
    for item in data['items']:
        tags.append({
            "tag": item['name'],
            "count": item['count']
        })
    return tags


# Route handler to fetch GitHub repositories
@router.get("/stackoverflow-tags")
async def stackoverflow_tags():
    tags = get_stackoverflow_tags()
    return {"tags": tags}