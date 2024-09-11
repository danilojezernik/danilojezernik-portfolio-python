import asyncio
import time
from fastapi import  HTTPException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import requests

from src.domain.language_data import LanguageData
from src.services import db
# Predefined list of programming languages you're interested in

# Max retry attempts for each page
MAX_RETRIES = 3
# Time to sleep between retries
RETRY_SLEEP_TIME = 2
# Number of pages to fetch
MAX_PAGES = 25

def fetch_stackoverflow_tags():
    url_template = 'https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&pagesize=100&page={}'
    page = 1
    filtered_tags = []
    total_fetched = 0

    while page <= MAX_PAGES:
        url = url_template.format(page)
        print(f"Fetching page {page} from StackOverflow API...")

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url, timeout=10)  # Set a timeout to avoid long waits

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Error fetching data from StackOverflow API")

                data = response.json()

                # Handle API errors
                if 'error_name' in data:
                    raise HTTPException(status_code=502, detail={
                        "error_id": data.get('error_id', 502),
                        "error_message": data.get('error_message', 'Unknown error'),
                        "error_name": data.get('error_name', 'unknown_error')
                    })

                # Track how many total items were fetched
                total_fetched += len(data.get('items', []))
                print(f"Fetched {len(data.get('items', []))} items, total fetched so far: {total_fetched}")

                # Add all tags from this page to the list
                for item in data.get('items', []):
                    tag_name = item['name'].lower()  # Make it case-insensitive
                    tag_count = item['count']
                    language_data = LanguageData(tag=tag_name, count=tag_count)
                    filtered_tags.append(language_data)
                    print(f"Found tag: {tag_name} with count: {tag_count}")

                # Move to the next page
                page += 1

                # If API rate-limits us, honor the backoff time
                if 'backoff' in data:
                    backoff_time = data['backoff']
                    print(f"Rate limited, backing off for {backoff_time} seconds")
                    time.sleep(backoff_time)

                # Break out of the retry loop if successful
                break

            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Request failed (attempt {retries}/{MAX_RETRIES}), error: {e}")
                if retries >= MAX_RETRIES:
                    raise HTTPException(status_code=500, detail=f"Failed to fetch data after {MAX_RETRIES} retries.")
                time.sleep(RETRY_SLEEP_TIME * retries)  # Exponential backoff between retries

            except Exception as e:
                # Handle unexpected exceptions and log the error
                print(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    print(f"Total tags fetched from page 1 to 24: {len(filtered_tags)}")

    # Insert or update tags in the database
    tags_dict = [tag.dict(by_alias=True) for tag in filtered_tags]

    if tags_dict:  # Only proceed if there are tags to insert
        db.process.language_data.delete_many({})  # Clear old data
        insert_result = db.process.language_data.insert_many(tags_dict)

        if insert_result.acknowledged:
            # Update the last_update field after inserting tags
            db.process.language_data.update_one(
                {},
                {"$set": {"last_update": datetime.utcnow()}},
                upsert=True  # Create the document if it doesn't exist
            )
            print(f"Inserted {len(insert_result.inserted_ids)} tags into the database.")
            return filtered_tags  # Return the filtered tags
        else:
            raise HTTPException(status_code=500, detail="Failed to insert tags into the database.")
    else:
        print("No tags found after pagination.")
        raise HTTPException(status_code=404, detail="No tags found.")


async def update_tags_in_db():
    print('Updating Stack Overflow tags in the database...')
    try:
        await asyncio.to_thread(fetch_stackoverflow_tags)  # Run in thread to avoid blocking event loop
        print('Tags updated successfully')
    except Exception as e:
        print(f'Error updating tags: {str(e)}')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(update_tags_in_db()), 'interval', hours=24)
    scheduler.start()