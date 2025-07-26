from pymongo import MongoClient

from src import env

# Technologies
from src.database.qa.angular import angular as angular_qa
from src.database.qa.javascript import javascript as javascript_qa
from src.database.qa.mongodb import mongodb as mongodb_qa
from src.database.qa.python import python as python_qa
from src.database.qa.typescript import typescript as typescript_qa
from src.database.qa.vue import vue as vue_qa

# Articles
from src.database.article.angular import angular as angular_articles
from src.database.article.javascript import javascript as javascript_articles
from src.database.article.mongodb import mongodb as mongodb_articles
from src.database.article.python import python as python_articles
from src.database.article.typescript import typescript as typescript_articles
from src.database.article.vue import vue as vue_articles

from src.database.sent_email_data import sent_email_data
from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.projects import projects
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]

def drop():
    # Dev APIs
    process.dev_api_angular.drop()
    process.dev_api_vue.drop()
    process.dev_api_typescript.drop()
    process.dev_api_python.drop()
    process.dev_api_javascript.drop()
    process.dev_api_mongodb.drop()

    # General
    process.blog.drop()
    process.sent_email_data.drop()
    process.message_reg.drop()
    process.links.drop()
    process.experiences.drop()
    process.contact.drop()
    process.projects.drop()
    process.subscriber.drop()
    process.comments.drop()
    process.book.drop()

    # Technologies
    process.angular_qa.drop()
    process.vue_qa.drop()
    process.typescript_qa.drop()
    process.javascript_qa.drop()
    process.python_qa.drop()
    process.mongodb_qa.drop()

    # Articles
    process.articles.drop()
    process.vue_articles.drop()
    process.typescript_articles.drop()
    process.javascript_articles.drop()
    process.python_articles.drop()
    process.mongodb_articles.drop()

    # Other
    process.language_data.drop()
    pass


def drop_user():
    process.user.drop()
    pass


def seed():
    # General
    process.blog.insert_many(blog)
    process.sent_email_data.insert_many(sent_email_data)
    process.links.insert_many(links)
    process.experiences.insert_many(experiences)
    process.contact.insert_many(contact)
    process.projects.insert_many(projects)
    process.book.insert_many(book)

    # Technologies
    process.angular_qa.insert_many(angular_qa)
    process.vue_qa.insert_many(vue_qa)
    process.typescript_qa.insert_many(typescript_qa)
    process.javascript_qa.insert_many(javascript_qa)
    process.python_qa.insert_many(python_qa)
    process.mongodb_qa.insert_many(mongodb_qa)

    # Articles
    process.angular_articles.insert_many(angular_articles)
    process.vue_articles.insert_many(vue_articles)
    process.typescript_articles.insert_many(typescript_articles)
    process.javascript_articles.insert_many(javascript_articles)
    process.python_articles.insert_many(python_articles)
    process.mongodb_articles.insert_many(mongodb_articles)
    pass


def seed_user():
    process.user.insert_many(user)
    pass

def drop_all_collections():
    """
    Drops all collections in the database instead of the whole DB.
    """
    for collection_name in process.list_collection_names():
        process[collection_name].drop()
