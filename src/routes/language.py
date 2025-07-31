from fastapi import APIRouter, Depends
from datetime import datetime, timedelta

from src.domain.language_data import LanguageData
from src.domain.user import User
from src.language_groups.languages_of_interests import LANGUAGES_OF_INTEREST, FRAMEWORKS_FRONTEND, FRAMEWORKS_BACKEND, \
    MOBILE_DEVELOPMENT, DATABASE_AND_DATA_MANAGEMENT, CLOUD_AND_DEVOPS, UI_UX_AND_DESIGN, TESTING_AND_AUTOMATION, \
    VERSION_CONTROL_AND_COLLABORATION, OPERATING_SYSTEMS_AND_PLATFORMS, TOOLS_AND_IDES
from src.services import db
from src.services.language_manager import update_tags_in_db, start_scheduler
from src.services.security import get_current_user

router = APIRouter()


# This route fetches tags and updates them if they are older than 24 hours
@router.get('/tags', operation_id='get_tags')
async def get_tags():
    """
    Fetches tags from the database. If the data is older than 24 hours, it triggers an update
    by calling the update_tags_in_db function.

    Returns:
        - If data is less than 24 hours old, it returns the cached data from the database.
        - If data is older than 24 hours, it updates the data by calling the external API and then returns the fresh data.
    """
    # Fetch the last time the data was updated (last_update) from the database
    last_update = db.process.language_data.find_one({}, {"_id": 0, "last_update": 1})

    # Get the current time in UTC
    current_time = datetime.utcnow()

    # Check if the data in the database is still fresh (updated in the last 24 hours)
    if last_update and (current_time - last_update['last_update']) < timedelta(hours=24):
        # If the data is fresh, fetch all tags from the database without updating
        tags = list(db.process.language_data.find({}, {"_id": 0, "tag": 1, "count": 1}))
        return tags
    else:
        # If the data is stale (older than 24 hours), trigger an update from the external API
        await update_tags_in_db()

        # After updating, fetch the newly updated tags from the database
        tags = list(db.process.language_data.find({}, {"_id": 0, "tag": 1, "count": 1}))
        return tags


# This route is for fetching all the tags, without any update logic
@router.get('/', operation_id='get_tags_preview')
async def get_language_tags_preview(current_user: User = Depends(get_current_user)):
    """
    Fetches a preview of all language tags from the database.

    Returns:
        - A list of LanguageData objects, each representing a programming language tag and its count.
    """
    # Fetch all documents (language tags) from the database
    cursor = db.process.language_data.find()

    # Convert each document from the cursor to a LanguageData object
    return [LanguageData(**document) for document in cursor]


# This function is called when the FastAPI app starts
@router.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.

    Starts the background scheduler that updates the Stack Overflow tags every 24 hours.
    This ensures that the data in the database stays up-to-date without requiring manual triggers.
    """
    # Start the background scheduler to trigger the update process every 24 hours
    start_scheduler()


# Route to fetch tags that belong to the list of programming languages of interest
@router.get('/programming-languages', operation_id='get_languages_of_interest')
async def get_languages_of_interest():
    """
    Fetches tags related to programming languages of interest from the database.

    Returns:
        - A list of LanguageData objects containing only the relevant programming languages.
    """
    # Query the database to find all documents (tags) where the 'tag' is in the LANGUAGES_OF_INTEREST list
    cursor = db.process.language_data.find({"tag": {"$in": LANGUAGES_OF_INTEREST}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch frontend frameworks from the database
@router.get('/frameworks-frontend', operation_id='get_frameworks_frontend')
async def get_frameworks_frontend():
    """
    Fetches tags related to frontend frameworks from the database.

    Returns:
        - A list of LanguageData objects containing only frontend frameworks.
    """
    # Query the database to find all documents where the 'tag' is in the FRAMEWORKS_FRONTEND list
    cursor = db.process.language_data.find({"tag": {"$in": FRAMEWORKS_FRONTEND}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch backend frameworks from the database
@router.get('/frameworks-backend', operation_id='get_frameworks_backend')
async def get_frameworks_backend():
    """
    Fetches tags related to backend frameworks from the database.

    Returns:
        - A list of LanguageData objects containing only backend frameworks.
    """
    # Query the database to find all documents where the 'tag' is in the FRAMEWORKS_BACKEND list
    cursor = db.process.language_data.find({"tag": {"$in": FRAMEWORKS_BACKEND}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to mobile development
@router.get('/mobile-development', operation_id='get_mobile_dev')
async def get_mobile_dev():
    """
    Fetches tags related to mobile development technologies from the database.

    Returns:
        - A list of LanguageData objects containing only mobile development tags.
    """
    # Query the database to find all documents where the 'tag' is in the MOBILE_DEVELOPMENT list
    cursor = db.process.language_data.find({"tag": {"$in": MOBILE_DEVELOPMENT}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to databases and data management
@router.get('/database-management', operation_id='get_database')
async def get_database():
    """
    Fetches tags related to databases and data management technologies from the database.

    Returns:
        - A list of LanguageData objects containing only database-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the DATABASE_AND_DATA_MANAGEMENT list
    cursor = db.process.language_data.find({"tag": {"$in": DATABASE_AND_DATA_MANAGEMENT}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to cloud and DevOps technologies
@router.get('/devops', operation_id='get_devops')
async def get_devops():
    """
    Fetches tags related to cloud and DevOps technologies from the database.

    Returns:
        - A list of LanguageData objects containing only cloud and DevOps-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the CLOUD_AND_DEVOPS list
    cursor = db.process.language_data.find({"tag": {"$in": CLOUD_AND_DEVOPS}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to UI/UX and design technologies
@router.get('/ui-ux-design', operation_id='get_ui_ux_design')
async def get_ui_ux_design():
    """
    Fetches tags related to UI/UX design technologies from the database.

    Returns:
        - A list of LanguageData objects containing only UI/UX design-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the UI_UX_AND_DESIGN list
    cursor = db.process.language_data.find({"tag": {"$in": UI_UX_AND_DESIGN}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to testing and automation technologies
@router.get('/testing', operation_id='get_testing')
async def get_testing():
    """
    Fetches tags related to testing and automation technologies from the database.

    Returns:
        - A list of LanguageData objects containing only testing and automation-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the TESTING_AND_AUTOMATION list
    cursor = db.process.language_data.find({"tag": {"$in": TESTING_AND_AUTOMATION}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to version control and collaboration tools
@router.get('/version-control', operation_id='get_version_control')
async def get_version_control():
    """
    Fetches tags related to version control and collaboration tools from the database.

    Returns:
        - A list of LanguageData objects containing only version control and collaboration-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the VERSION_CONTROL_AND_COLLABORATION list
    cursor = db.process.language_data.find({"tag": {"$in": VERSION_CONTROL_AND_COLLABORATION}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to operating systems and platforms
@router.get('/operating-system', operation_id='get_operating_system')
async def get_operating_system():
    """
    Fetches tags related to operating systems and platforms from the database.

    Returns:
        - A list of LanguageData objects containing only operating systems and platforms-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the OPERATING_SYSTEMS_AND_PLATFORMS list
    cursor = db.process.language_data.find({"tag": {"$in": OPERATING_SYSTEMS_AND_PLATFORMS}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]


# Route to fetch tags related to development tools and IDEs
@router.get('/ides', operation_id='get_ides')
async def get_ides():
    """
    Fetches tags related to development tools and IDEs from the database.

    Returns:
        - A list of LanguageData objects containing only development tools and IDE-related tags.
    """
    # Query the database to find all documents where the 'tag' is in the TOOLS_AND_IDES list
    cursor = db.process.language_data.find({"tag": {"$in": TOOLS_AND_IDES}})

    # Return the result as a list of LanguageData objects
    return [LanguageData(**document) for document in cursor]
