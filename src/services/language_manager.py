import asyncio

from fastapi import  HTTPException
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import requests

from src.domain.language_data import LanguageData
from src.services import db

# Function to fetch popular tags from Stack Overflow API
def fetch_stackoverflow_tags():
    url = 'https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow'
    response = requests.get(url)
    data = response.json()

    # Handle error from the API, like throttle_violation
    if 'error_name' in data:
        raise HTTPException(status_code=502, detail={
            "error_id": data.get('error_id', 502),
            "error_message": data.get('error_message', 'Unknown error'),
            "error_name": data.get('error_name', 'unknown_error')
        })

    tags: list[LanguageData] = []

    for item in data['items']:
        tag_name = item['name']
        tag_count = item['count']
        language_data = LanguageData(tag=tag_name, count=tag_count)
        tags.append(language_data)

    tags_dict = [tag.dict(by_alias=True) for tag in tags]

    db.process.language_data.delete_many({})
    insert_result = db.process.language_data.insert_many(tags_dict)

    if insert_result.acknowledged:
        # Update the last_update field after inserting tags
        db.process.language_data.update_one(
            {},
            {"$set": {"last_update": datetime.utcnow()}},
            upsert=True  # Create the document if it doesn't exist
        )
        print(f"Inserted {len(insert_result.inserted_ids)} tags into the database.")
        return tags  # Return the list of inserted tags
    else:
        # Handle failure in insertion
        raise HTTPException(status_code=500, detail="Failed to insert tags into the database.")


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