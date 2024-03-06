from pymongo import MongoClient

from src import env

from src.database.blog import blog
from src.database.experiences import experiences
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    process.experiences.drop()
    pass

def drop_user():
    process.user.drop()
    pass

def seed():
    process.blog.insert_many(blog)
    process.experiences.insert_many(experiences)
    pass

def seed_user():
    process.user.insert_many(user)
    pass