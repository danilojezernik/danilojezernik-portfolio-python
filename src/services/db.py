from pymongo import MongoClient

from src import env

# Technologies
from src.database.angular import angular
from src.database.javascript import javascript
from src.database.mongodb import mongodb
from src.database.python import python
from src.database.typescript import typescript
from src.database.vue import vue
from src.database.sent_email_data import sent_email_data
from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.newsletter import newsletter
from src.database.projects import projects
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]

def drop():
    process.dev_api_angular.drop()
    process.dev_api_vue.drop()
    process.dev_api_typescript.drop()
    process.dev_api_python.drop()
    process.dev_api_javascript.drop()
    process.dev_api_mongodb.drop()
    process.blog.drop()
    process.sent_email_data.drop()
    process.message_reg.drop()
    process.links.drop()
    process.experiences.drop()
    process.contact.drop()
    process.projects.drop()
    process.newsletter.drop()
    process.subscriber.drop()
    process.comments.drop()
    process.book.drop()

    # Technologies
    process.angular.drop()
    process.vue.drop()
    process.typescript.drop()
    process.javascript.drop()
    process.python.drop()
    process.mongodb.drop()

    # Drop language_data collection
    process.language_data.drop()
    pass


def drop_user():
    process.user.drop()
    pass


def seed():
    process.blog.insert_many(blog)
    process.sent_email_data.insert_many(sent_email_data)
    process.links.insert_many(links)
    process.experiences.insert_many(experiences)
    process.contact.insert_many(contact)
    process.projects.insert_many(projects)
    process.newsletter.insert_many(newsletter)
    process.book.insert_many(book)

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
