from fastapi.testclient import TestClient

from src.domain.language import Language
from src.domain.article import Article
from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.experiences import Experiences
from src.domain.links import Links
from src.domain.projects import Projects
from src import env

from src.test.utils.helpers import check_status_response_for, check_health, check_status_response_by_id_for, \
    login_success_helper, login_failed_helper

from src.__main__ import app

client = TestClient(app)


# Test check
def test_return_healthy_check(mongodb):
    check_health('healthy')


# Blog
def test_route_blog(mongodb):
    check_status_response_for('blog', Blog)


def test_route_blog_by_id(mongodb):
    check_status_response_by_id_for('blog', Blog)


# Book
def test_route_book(mongodb):
    check_status_response_for('book', Book)


def test_route_book_by_id(mongodb):
    check_status_response_by_id_for('book', Book)


# Links
def test_route_link(mongodb):
    check_status_response_for('links', Links)


def test_route_links_by_id(mongodb):
    check_status_response_by_id_for('links', Links)


# Projects
def test_route_projects(mongodb):
    check_status_response_for('projects', Projects)


def test_route_projects_by_id(mongodb):
    check_status_response_by_id_for('projects', Projects)


# Experiences
def test_route_experiences(mongodb):
    check_status_response_for('experiences', Experiences)


def test_route_experiences_by_id(mongodb):
    check_status_response_by_id_for('experiences', Experiences)


# MongoDB
## QA
def test_route_qa_mongodb(mongodb):
    check_status_response_for('/qa/mongodb', Language)


def test_route_qa_mongodb_by_id(mongodb):
    check_status_response_by_id_for('/qa/mongodb', Language)


## Article
def test_route_article_mongodb(mongodb):
    check_status_response_for('/article/mongodb', Article)


def test_route_article_mongodb_by_id(mongodb):
    check_status_response_by_id_for('/article/mongodb', Article)


# Python
## QA
def test_route_qa_python(mongodb):
    check_status_response_for('/qa/python', Language)


def test_route_qa_python_by_id(mongodb):
    check_status_response_by_id_for('/qa/python', Language)


## Article
def test_route_article_python(mongodb):
    check_status_response_for('/article/python', Article)


def test_route_article_python_by_id(mongodb):
    check_status_response_by_id_for('/article/python', Article)


# TypeScript
## QA
def test_route_qa_typescript(mongodb):
    check_status_response_for('/qa/typescript', Language)


def test_route_qa_typescript_by_id(mongodb):
    check_status_response_by_id_for('/qa/typescript', Language)


## Article
def test_route_article_typescript(mongodb):
    check_status_response_for('/article/typescript', Article)


def test_route_article_typescript_by_id(mongodb):
    check_status_response_by_id_for('/article/typescript', Article)


# JavaScript
## QA
def test_route_qa_javascript(mongodb):
    check_status_response_for('/qa/javascript', Language)


def test_route_qa_javascript_by_id(mongodb):
    check_status_response_by_id_for('/qa/javascript', Language)


## Article
def test_route_article_javascript(mongodb):
    check_status_response_for('/article/javascript', Article)


def test_route_article_javascript_by_id(mongodb):
    check_status_response_by_id_for('/article/javascript', Article)


# Vue
## QA
def test_route_qa_vue(mongodb):
    check_status_response_for('/qa/vue', Language)


def test_route_qa_vue_by_id(mongodb):
    check_status_response_by_id_for('/qa/vue', Language)


## Article
def test_route_article_vue(mongodb):
    check_status_response_for('/article/vue', Article)


def test_route_article_vue_by_id(mongodb):
    check_status_response_by_id_for('/article/vue', Article)


# Angular
## QA
def test_route_qa_angular(mongodb):
    check_status_response_for('/qa/angular', Language)


def test_route_qa_angular_by_id(mongodb):
    check_status_response_by_id_for('/qa/angular', Language)


# Cypress
## QA
def test_route_qa_cypress(mongodb):
    check_status_response_for('/qa/cypress', Language)


def test_route_qa_cypress_by_id(mongodb):
    check_status_response_by_id_for('/qa/cypress', Language)


# Article
def test_route_article_cypress(mongodb):
    check_status_response_for('/article/cypress', Article)


def test_route_article_cypress_by_id(mongodb):
    check_status_response_by_id_for('/article/cypress', Article)


# Django
## QA
def test_route_qa_django(mongodb):
    check_status_response_for('/qa/django', Language)


def test_route_qa_django_by_id(mongodb):
    check_status_response_by_id_for('/qa/django', Language)


# Article
def test_route_article_django(mongodb):
    check_status_response_for('/article/django', Article)


def test_route_article_django_by_id(mongodb):
    check_status_response_by_id_for('/article/django', Article)


# Docker
## QA
def test_route_qa_docker(mongodb):
    check_status_response_for('/qa/docker', Language)


def test_route_qa_docker_by_id(mongodb):
    check_status_response_by_id_for('/qa/docker', Language)


# Article
def test_route_article_docker(mongodb):
    check_status_response_for('/article/docker', Article)


def test_route_article_docker_by_id(mongodb):
    check_status_response_by_id_for('/article/docker', Article)


# Nuxt
## QA
def test_route_qa_nuxt(mongodb):
    check_status_response_for('/qa/nuxt', Language)


def test_route_qa_nuxt_by_id(mongodb):
    check_status_response_by_id_for('/qa/nuxt', Language)


# Article
def test_route_article_nuxt(mongodb):
    check_status_response_for('/article/nuxt', Article)


def test_route_article_nuxt_by_id(mongodb):
    check_status_response_by_id_for('/article/nuxt', Article)


# Pytest
## QA
def test_route_qa_pytest(mongodb):
    check_status_response_for('/qa/pytest', Language)


def test_route_qa_pytest_by_id(mongodb):
    check_status_response_by_id_for('/qa/pytest', Language)


# Article
def test_route_article_pytest(mongodb):
    check_status_response_for('/article/pytest', Article)


def test_route_article_pytest_by_id(mongodb):
    check_status_response_by_id_for('/article/pytest', Article)


# Tailwind
## QA
def test_route_qa_tailwind(mongodb):
    check_status_response_for('/qa/tailwind', Language)


def test_route_qa_tailwind_by_id(mongodb):
    check_status_response_by_id_for('/qa/tailwind', Language)


# Article
def test_route_article_tailwind(mongodb):
    check_status_response_for('/article/tailwind', Article)


def test_route_article_tailwind_by_id(mongodb):
    check_status_response_by_id_for('/article/tailwind', Article)


# SQL
## QA
def test_route_qa_sql(mongodb):
    check_status_response_for('/qa/sql', Language)


def test_route_qa_sql_by_id(mongodb):
    check_status_response_by_id_for('/qa/sql', Language)


# Article
def test_route_article_sql(mongodb):
    check_status_response_for('/article/sql', Article)


def test_route_article_sql_by_id(mongodb):
    check_status_response_by_id_for('/article/sql', Article)


# FastAPI
## QA
def test_route_qa_fastapi(mongodb):
    check_status_response_for('/qa/fastapi', Language)


def test_route_qa_fastapi_by_id(mongodb):
    check_status_response_by_id_for('/qa/fastapi', Language)


# Article
def test_route_article_fastapi(mongodb):
    check_status_response_for('/article/fastapi', Article)


def test_route_article_fastapi_by_id(mongodb):
    check_status_response_by_id_for('/article/fastapi', Article)


# Playwright
## QA
def test_route_qa_playwright(mongodb):
    check_status_response_for('/qa/playwright', Language)


def test_route_qa_playwright_by_id(mongodb):
    check_status_response_by_id_for('/qa/playwright', Language)


# Article
def test_route_article_playwright(mongodb):
    check_status_response_for('/article/playwright', Article)


def test_route_article_playwright_by_id(mongodb):
    check_status_response_by_id_for('/article/playwright', Article)


def test_login_success(monkeypatch):
    login_success_helper(monkeypatch, env.USERNAME, env.PASSWORD_LOGIN)


def test_login_failure(monkeypatch):
    login_failed_helper(monkeypatch, 'napaka', 'napaka')
