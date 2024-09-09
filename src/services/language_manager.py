import asyncio
from fastapi import HTTPException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from src.domain.language_data import LanguageData
from src.services import db

# Function to fetch popular tags from Stack Overflow API
def fetch_stackoverflow_tags():
    """
    Fetches the most popular tags from Stack Overflow API,
    processes them into LanguageData objects, and updates the database.
    """
    # URL to get popular tags from Stack Overflow API
    url = 'https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow'

    # Send GET request to the Stack Overflow API
    response = requests.get(url)

    # Parse the JSON response from the API
    data = response.json()

    # Check if there was an error in the API response (e.g., rate limit exceeded)
    if 'error_name' in data:
        raise HTTPException(
            status_code=502,
            detail={
                "error_id": data.get('error_id', 502),
                "error_message": data.get('error_message', 'Unknown error'),
                "error_name": data.get('error_name', 'unknown_error')
            }
        )

    # Initialize an empty list to store the tags
    tags: list[LanguageData] = []

    # Loop through each item (tag) in the API response
    for item in data['items']:
        # Extract tag name and count from the API response
        tag_name = item['name']
        tag_count = item['count']

        # Create a LanguageData object for each tag
        language_data = LanguageData(tag=tag_name, count=tag_count)

        # Append the LanguageData object to the tags list
        tags.append(language_data)

    # Convert the list of LanguageData objects to dictionaries for MongoDB insertion
    tags_dict = [tag.dict(by_alias=True) for tag in tags]

    # Clear existing tags from the database before inserting new ones
    db.process.language_data.delete_many({})

    # Insert the new tags into the database
    insert_result = db.process.language_data.insert_many(tags_dict)

    # If insertion is acknowledged by the database
    if insert_result.acknowledged:
        # Update the 'last_update' field with the current timestamp after successful insertion
        db.process.language_data.update_one(
            {},
            {"$set": {"last_update": datetime.utcnow()}},
            upsert=True  # Create the document if it doesn't exist
        )
        # Log the number of tags inserted and return the inserted tags
        print(f"Inserted {len(insert_result.inserted_ids)} tags into the database.")
        return tags  # Return the list of inserted tags
    else:
        # If the insertion failed, raise an HTTPException with status 500
        raise HTTPException(status_code=500, detail="Failed to insert tags into the database.")


# Asynchronous function to update tags in the database
async def update_tags_in_db():
    """
    Asynchronously updates the tags in the database by calling the fetch_stackoverflow_tags function.
    This function is meant to run periodically and ensures the database is up-to-date.
    """
    print('Updating Stack Overflow tags in the database...')
    try:
        # Run the fetch_stackoverflow_tags function in a separate thread to avoid blocking the event loop
        await asyncio.to_thread(fetch_stackoverflow_tags)
        print('Tags updated successfully')
    except Exception as e:
        # Catch and log any errors that occur during the update
        print(f'Error updating tags: {str(e)}')


# Function to start the background scheduler for updating tags every 24 hours
def start_scheduler():
    """
    Starts a background scheduler that updates the Stack Overflow tags every 24 hours.
    It runs the update_tags_in_db function periodically.
    """
    # Initialize the background scheduler
    scheduler = BackgroundScheduler()

    # Add a job to run update_tags_in_db every 24 hours
    scheduler.add_job(lambda: asyncio.run(update_tags_in_db()), 'interval', hours=24)

    # Start the scheduler
    scheduler.start()
