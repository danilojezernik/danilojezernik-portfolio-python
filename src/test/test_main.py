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


## Article
def test_route_article_angular(mongodb):
    check_status_response_for('/article/angular', Article)


def test_route_article_angular_by_id(mongodb):
    check_status_response_by_id_for('/article/angular', Article)


def test_login_success(monkeypatch):
    login_success_helper(monkeypatch, env.USERNAME, env.PASSWORD_LOGIN)


def test_login_failure(monkeypatch):
    login_failed_helper(monkeypatch, 'napaka', 'napaka')
