from pymongo import MongoClient

from src import env

from src.database.blog import blog
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.projects import projects
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    process.links.drop()
    process.experiences.drop()
    process.contact.drop()
    process.projects.drop()
    pass


def drop_user():
    process.user.drop()
    pass


def seed():
    process.blog.insert_many(blog)
    process.links.insert_many(links)
    process.experiences.insert_many(experiences)
    process.contact.insert_many(contact)
    process.projects.insert_many(projects)
    pass


def seed_user():
    process.user.insert_many(user)
    pass
