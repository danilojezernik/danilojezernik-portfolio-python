from pymongo import MongoClient

from src import env

from src.database.blog import blog

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    pass


def seed():
    process.blog.insert_many(blog)
    pass
