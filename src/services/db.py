from pymongo import MongoClient
from src import env

# User data and all seedable collections
from src.database.user import user
from src.services.collections import collections

# ---------------------------------------------------------------------------
# Database client setup
# ---------------------------------------------------------------------------
# Use development MongoDB connection if in development mode, otherwise use production
if env.ENV.lower() == 'development':
    print(f"Using development MongoDB connection: {env.DB_DEV}")
    client = MongoClient(env.DB_DEV)  # Connect to local MongoDB instance
else:
    print(f"Using production MongoDB connection")
    client = MongoClient(env.DB_MAIN)  # Connect to production MongoDB instance

process = client[env.DB_PROCESS]  # Select the database


# ---------------------------------------------------------------------------
# DROP FUNCTIONS
# ---------------------------------------------------------------------------
def drop():
    """
    Drops all pre-defined collections in the `collections` dictionary and
    also clears special 'dev' and other standalone collections.
    """
    # Drop Dev API collections (not part of the collections dict)
    special_dev_collections = [
        "dev_api_angular", "dev_api_vue", "dev_api_typescript",
        "dev_api_python", "dev_api_javascript", "dev_api_mongodb"
    ]

    for dev_collection in special_dev_collections:
        if dev_collection in process.list_collection_names():
            process[dev_collection].drop()
            print(f"Dropped special collection: {dev_collection}")

    # Drop other standalone collections
    if "language_data" in process.list_collection_names():
        process.language_data.drop()
        print("Dropped special collection: language_data")

    # Drop collections defined in `collections` dict
    for collection_name in collections.keys():
        if collection_name in process.list_collection_names():
            process[collection_name].drop()
            print(f"Dropped collection: {collection_name}")


def drop_user():
    """
    Drops the user collection only.
    """
    if "user" in process.list_collection_names():
        process.user.drop()
        print("Dropped user collection")


def drop_all_collections():
    """
    Drops ALL collections in the database.
    Use with caution!
    """
    for collection_name in process.list_collection_names():
        process[collection_name].drop()
        print(f"Dropped collection: {collection_name}")


# ---------------------------------------------------------------------------
# SEED FUNCTIONS
# ---------------------------------------------------------------------------
def seed():
    """
    Inserts seed data into all collections defined in the `collections` dict.
    """
    for collection_name, data in collections.items():
        if data:  # Only insert if seed data exists
            process[collection_name].insert_many(data)
            print(f"Seeded collection: {collection_name}")


def seed_user():
    """
    Seeds the user collection with user data.
    """
    if user:
        process.user.insert_many(user)
        print("Seeded user collection")
