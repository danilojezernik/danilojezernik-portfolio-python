from pymongo import MongoClient

from src import env

from src.database.blog import blog
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.user.drop()
    process.blog.drop()
    pass


def seed():
    process.user.insert_many(user)
    process.blog.insert_many(blog)
    pass
