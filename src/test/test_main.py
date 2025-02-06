from fastapi.testclient import TestClient

from src.domain.angular import Angular
from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.experiences import Experiences
from src.domain.javascript import JavaScript
from src.domain.links import Links
from src.domain.mongodb import MongoDb
from src.domain.projects import Projects
from src.domain.python import Python
from src.domain.typescript import TypeScript
from src.domain.vue import Vue
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
def test_route_mongodb(mongodb):
    check_status_response_for('mongodb', MongoDb)


def test_route_mongodb_by_id(mongodb):
    check_status_response_by_id_for('mongodb', MongoDb)


# Python
def test_route_python(mongodb):
    check_status_response_for('python', Python)


def test_route_python_by_id(mongodb):
    check_status_response_by_id_for('python', Python)


# TypeScript
def test_route_typescript(mongodb):
    check_status_response_for('typescript', TypeScript)


def test_route_typescript_by_id(mongodb):
    check_status_response_by_id_for('typescript', TypeScript)


# JavaScript
def test_route_javascript(mongodb):
    check_status_response_for('javascript', JavaScript)


def test_route_javascript_by_id(mongodb):
    check_status_response_by_id_for('javascript', JavaScript)


# Vue
def test_route_vue(mongodb):
    check_status_response_for('vue', Vue)


def test_route_vue_by_id(mongodb):
    check_status_response_by_id_for('vue', Vue)


# Angular
def test_route_angular(mongodb):
    check_status_response_for('angular', Angular)


def test_route_angular_by_id(mongodb):
    check_status_response_by_id_for('angular', Angular)


def test_login_success(monkeypatch):
    login_success_helper(monkeypatch, env.USERNAME, env.PASSWORD_LOGIN)


def test_login_failure(monkeypatch):
    login_failed_helper(monkeypatch, 'napaka', 'napaka')
