from fastapi.testclient import TestClient

from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.links import Links

from src.test.utils.helpers import check_status_response_for, check_health

from src.__main__ import app

client = TestClient(app)


def test_return_healthy_check():
    check_health('healthy')


def test_route_blog(mongodb):
    check_status_response_for('blog', Blog)


def test_route_book(mongodb):
    check_status_response_for('book', Book)


def test_route_link(mongodb):
    check_status_response_for('links', Links)

