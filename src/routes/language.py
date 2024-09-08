# Import necessary modules and libraries
from fastapi import APIRouter, HTTPException
import datetime
import logging

import requests

from src.domain.language_data import LanguageData, LanguageDataResponse
from src.services import db

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to fetch popular tags from Stack Overflow API
def fetch_stackoverflow_tags():
    url = 'https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow'
    response = requests.get(url)
    data = response.json()

    # Handle error from the API, like throttle_violation
    if 'error_name' in data:
        logging.error(f"Error fetching StackOverflow tags: {data.get('error_message')}")
        raise HTTPException(status_code=502, detail={
            "error_id": data.get('error_id', 502),
            "error_message": data.get('error_message', 'Unknown error'),
            "error_name": data.get('error_name', 'unknown_error')
        })

    tags = [LanguageData(tag=item['name'], count=item['count']) for item in data['items']]
    return tags

# Function to store/update tags in MongoDB with a timestamp
def store_tags_in_db(tags):
    now = datetime.datetime.utcnow()
    try:
        db.process.language_data.update_one(
            {"data_type": "stackoverflow_tags"},  # Ensure we only store one set of tags
            {
                "$set": {
                    "tags": [tag.dict() for tag in tags],  # Convert Pydantic models to dicts
                    "last_updated": now
                }
            },
            upsert=True  # Insert new if doesn't exist
        )
        logging.info(f"Tags successfully stored/updated in the database at {now}")
    except Exception as e:
        logging.error(f"Error storing tags in the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

# Function to check if the data in the database is older than 24 hours
def is_data_stale():
    try:
        data = db.process.language_data.find_one({"data_type": "stackoverflow_tags"})
        if data:
            last_updated = data.get("last_updated")
            if last_updated:
                # Calculate the time difference
                time_difference = datetime.datetime.utcnow() - last_updated
                # Check if it's more than 24 hours (86400 seconds)
                if time_difference.total_seconds() > 86400:
                    return True
                return False
        return True  # No data in the database, so it's stale
    except Exception as e:
        logging.error(f"Error checking data freshness in the database: {str(e)}")
        return True  # Treat as stale if there's a database error

# Route handler to fetch tags from Stack Overflow or retrieve from the database
@router.get("/stackoverflow-tags", response_model=LanguageDataResponse)
async def stackoverflow_tags():
    # Check if the data is stale (older than 24 hours)
    if is_data_stale():
        logging.info("Data is stale, fetching new tags from Stack Overflow API...")
        # Fetch new data from the API
        tags = fetch_stackoverflow_tags()
        # Store the data in the database
        store_tags_in_db(tags)
    else:
        logging.info("Fetching tags from the database...")
        # Get the data from the database
        data = db.process.language_data.find_one({"data_type": "stackoverflow_tags"})
        tags = [LanguageData(**tag) for tag in data["tags"]]

    return LanguageDataResponse(tags=tags)