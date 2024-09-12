import asyncio
import time
from fastapi import  HTTPException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import requests

from src import env
from src.domain.language_data import LanguageData
from src.services import db

MAX_RETRIES = 3  # Maximum number of retries for each page if a request fails
RETRY_SLEEP_TIME = 2  # Time (in seconds) to wait before retrying a failed request, with exponential backoff
MAX_PAGES = 25  # Maximum number of pages allowed (as per StackOverflow API limitations)

# Function to fetch tags from StackOverflow API
def fetch_stackoverflow_tags():
    """
    Fetches tags from the StackOverflow API and processes the data.

    The function fetches tags from multiple pages of the API, up to the limit of MAX_PAGES.
    In case of request failures, it retries up to MAX_RETRIES times with exponential backoff.
    Tags are inserted into the database after fetching all pages.

    Returns:
        A list of filtered tags (LanguageData objects) inserted into the database.
    """
    url_template = env.STACK_URL  # URL template with placeholders for the page number
    page = 1  # Start from the first page
    filtered_tags = []  # List to store fetched tags
    total_fetched = 0  # Counter to keep track of the total number of fetched tags

    # Loop through pages, up to the allowed MAX_PAGES limit
    while page <= MAX_PAGES:
        url = url_template.format(page)  # Format the URL with the current page number
        print(f"Fetching page {page} from StackOverflow API...")

        retries = 0  # Initialize the retry counter for each page
        while retries < MAX_RETRIES:
            try:
                # Send the request to StackOverflow API with a timeout of 10 seconds
                response = requests.get(url, timeout=10)

                # If the response status is not 200 (OK), raise an HTTPException
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Error fetching data from StackOverflow API")

                # Parse the JSON response
                data = response.json()

                # Check for errors in the API response (such as throttle violations)
                if 'error_name' in data:
                    raise HTTPException(status_code=502, detail={
                        "error_id": data.get('error_id', 502),
                        "error_message": data.get('error_message', 'Unknown error'),
                        "error_name": data.get('error_name', 'unknown_error')
                    })

                # Track how many items were fetched from this page
                total_fetched += len(data.get('items', []))
                print(f"Fetched {len(data.get('items', []))} items, total fetched so far: {total_fetched}")

                # Add each tag from the fetched items to the filtered_tags list
                for item in data.get('items', []):
                    tag_name = item['name'].lower()  # Convert tag name to lowercase for consistency
                    tag_count = item['count']  # Get the count of occurrences for this tag
                    language_data = LanguageData(tag=tag_name, count=tag_count)
                    filtered_tags.append(language_data)
                    print(f"Found tag: {tag_name} with count: {tag_count}")

                # Move to the next page
                page += 1

                # Handle API rate-limiting by honoring the 'backoff' time if provided
                if 'backoff' in data:
                    backoff_time = data['backoff']
                    print(f"Rate limited, backing off for {backoff_time} seconds")
                    time.sleep(backoff_time)

                # Break out of the retry loop if the request is successful
                break

            except requests.exceptions.RequestException as e:
                # Handle request-related exceptions (network errors, timeouts, etc.)
                retries += 1
                print(f"Request failed (attempt {retries}/{MAX_RETRIES}), error: {e}")
                if retries >= MAX_RETRIES:
                    # If maximum retries are exhausted, raise an exception
                    raise HTTPException(status_code=500, detail=f"Failed to fetch data after {MAX_RETRIES} retries.")
                # Wait before retrying (exponential backoff)
                time.sleep(RETRY_SLEEP_TIME * retries)

            except Exception as e:
                # Handle unexpected errors
                print(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    print(f"Total tags fetched from page 1 to {MAX_PAGES}: {len(filtered_tags)}")

    # Insert or update the fetched tags in the database
    tags_dict = [tag.dict(by_alias=True) for tag in filtered_tags]  # Convert the tags to dictionary format for insertion

    if tags_dict:  # Proceed only if there are tags to insert
        db.process.language_data.delete_many({})  # Clear old data in the language_data collection
        insert_result = db.process.language_data.insert_many(tags_dict)  # Insert the new tags

        if insert_result.acknowledged:
            # If insertion is successful, update the 'last_update' field with the current time
            db.process.language_data.update_one(
                {},
                {"$set": {"last_update": datetime.utcnow()}},
                upsert=True  # If the document doesn't exist, create it
            )
            print(f"Inserted {len(insert_result.inserted_ids)} tags into the database.")
            return filtered_tags  # Return the inserted tags
        else:
            # Handle database insertion failure
            raise HTTPException(status_code=500, detail="Failed to insert tags into the database.")
    else:
        # If no tags were found, raise an error
        print("No tags found after pagination.")
        raise HTTPException(status_code=404, detail="No tags found.")


# Function to trigger the update of tags in the database (runs in a thread to avoid blocking the event loop)
async def update_tags_in_db():
    print('Updating Stack Overflow tags in the database...')
    try:
        await asyncio.to_thread(fetch_stackoverflow_tags)  # Run the function in a separate thread
        print('Tags updated successfully')
    except Exception as e:
        print(f'Error updating tags: {str(e)}')


# Function to start a background scheduler that updates the tags every 24 hours
def start_scheduler():
    """
    Starts the background scheduler that updates the Stack Overflow tags every 24 hours.
    """
    scheduler = BackgroundScheduler()  # Initialize the scheduler
    scheduler.add_job(lambda: asyncio.run(update_tags_in_db()), 'interval', hours=24)  # Schedule the job to run every 24 hours
    scheduler.start()  # Start the scheduler
