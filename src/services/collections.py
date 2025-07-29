# Technologies
from src.database.qa.angular import angular as angular_qa
from src.database.qa.javascript import javascript as javascript_qa
from src.database.qa.mongodb import mongodb as mongodb_qa
from src.database.qa.python import python as python_qa
from src.database.qa.typescript import typescript as typescript_qa
from src.database.qa.vue import vue as vue_qa
from src.database.qa.cypress import cypress as cypress_qa
from src.database.qa.django import django as django_qa
from src.database.qa.docker import docker as docker_qa
from src.database.qa.nuxt import nuxt as nuxt_qa

# Articles
from src.database.article.angular import angular as angular_articles
from src.database.article.javascript import javascript as javascript_articles
from src.database.article.mongodb import mongodb as mongodb_articles
from src.database.article.python import python as python_articles
from src.database.article.typescript import typescript as typescript_articles
from src.database.article.vue import vue as vue_articles
from src.database.article.cypress import cypress as cypress_articles
from src.database.article.django import django as django_articles
from src.database.article.docker import docker as docker_articles
from src.database.article.nuxt import nuxt as nuxt_articles

from src.database.sent_email_data import sent_email_data
from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.projects import projects

collections = {
    # General
    "blog": blog,
    "sent_email_data": sent_email_data,
    "links": links,
    "experiences": experiences,
    "contact": contact,
    "projects": projects,
    "book": book,

    # Technologies - QA
    "angular_qa": angular_qa,
    "vue_qa": vue_qa,
    "typescript_qa": typescript_qa,
    "javascript_qa": javascript_qa,
    "python_qa": python_qa,
    "mongodb_qa": mongodb_qa,
    "cypress_qa": cypress_qa,
    "django_qa": django_qa,
    "docker_qa": docker_qa,
    "nuxt_qa": nuxt_qa,

    # Articles
    "angular_articles": angular_articles,
    "vue_articles": vue_articles,
    "typescript_articles": typescript_articles,
    "javascript_articles": javascript_articles,
    "python_articles": python_articles,
    "mongodb_articles": mongodb_articles,
    "cypress_articles": cypress_articles,
    "django_articles": django_articles,
    "docker_articles": docker_articles,
    "nuxt_articles": nuxt_articles,
}
