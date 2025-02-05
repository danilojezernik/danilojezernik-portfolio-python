import pytest
from src.services import db
from src.database.book import book


@pytest.fixture(scope='session')
def mongodb():
    client = db.client

    assert client.admin.command('ping')['ok'] != 0.0, "Unable to connect to MongoDB."
    return client

@pytest.fixture
def book_data():
    return book
