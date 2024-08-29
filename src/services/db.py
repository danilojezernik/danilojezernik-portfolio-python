from pymongo import MongoClient

from src import env

# Technologies
from src.database.angular import angular
from src.database.javascript import javascript
from src.database.mongodb import mongodb
from src.database.python import python
from src.database.typescript import typescript
from src.database.vue import vue

from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.newsletter import newsletter
from src.database.projects import projects
from src.database.subscriber import subscriber
from src.database.technology import technology
from src.database.user import user
from src.database.comments import comments

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    process.links.drop()
    process.experiences.drop()
    process.contact.drop()
    process.projects.drop()
    process.newsletter.drop()
    process.subscriber.drop()
    process.comments.drop()
    process.book.drop()
    # process.technology.drop()

    # Technologies
    process.angular.drop()
    process.vue.drop()
    process.typescript.drop()
    process.javascript.drop()
    process.python.drop()
    process.mongodb.drop()
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
    process.newsletter.insert_many(newsletter)
    process.subscriber.insert_many(subscriber)
    process.comments.insert_many(comments)
    process.book.insert_many(book)
    # process.technology.insert_many(technology)

    # Technologies
    process.angular.insert_many(angular)
    process.vue.insert_many(vue)
    process.typescript.insert_many(typescript)
    process.javascript.insert_many(javascript)
    process.python.insert_many(python)
    process.mongodb.insert_many(mongodb)
    pass


def seed_user():
    process.user.insert_many(user)
    pass
