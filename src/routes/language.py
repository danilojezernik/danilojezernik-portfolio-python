from fastapi import APIRouter
from datetime import datetime, timedelta

from src.domain.language_data import LanguageData
from src.services import db
from src.services.language_manager import update_tags_in_db, start_scheduler

router = APIRouter()


@router.get('/tags', operation_id='get_tags')
async def get_tags():
    """
    Fetches tags from the database. If the data is older than 24 hours, it triggers an update
    by calling the update_tags_in_db function.

    Returns:
        - If data is less than 24 hours old, it returns the cached data from the database.
        - If data is older than 24 hours, it updates the data by calling the external API and then returns the fresh data.
    """
    # Fetch the 'last_update' time from the database, which indicates when the data was last updated
    last_update = db.process.language_data.find_one({}, {"_id": 0, "last_update": 1})

    # Get the current time (UTC)
    current_time = datetime.utcnow()

    # Check if the data was updated within the last 24 hours
    if last_update and (current_time - last_update['last_update']) < timedelta(hours=24):
        # If data is fresh, return the existing tags from the database
        tags = list(db.process.language_data.find({}, {"_id": 0, "tag": 1, "count": 1}))
        return tags
    else:
        # If data is stale (older than 24 hours), trigger an update by calling the API
        await update_tags_in_db()

        # After updating, fetch the newly updated tags from the database
        tags = list(db.process.language_data.find({}, {"_id": 0, "tag": 1, "count": 1}))
        return tags


@router.get('/', operation_id='get_tags_preview')
async def get_language_tags_preview():
    """
    Fetches a preview of all language tags from the database.

    Returns:
        - A list of LanguageData objects, each representing a programming language tag and its count.
    """
    # Fetch all documents (language tags) from the database
    cursor = db.process.language_data.find()

    # Convert the documents to LanguageData objects and return them as a list
    return [LanguageData(**document) for document in cursor]


@router.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.

    Starts the background scheduler that updates the Stack Overflow tags every 24 hours.
    This ensures that the data in the database stays up-to-date without requiring manual triggers.
    """
    # Start the background scheduler to update tags every 24 hours
    start_scheduler()