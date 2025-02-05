from typing import Type
from pydantic import BaseModel
from fastapi.testclient import TestClient
from src.services import db
from src.__main__ import app
from fastapi import status
from typing import Optional

client = TestClient(app)


def normalize_data(data, model: Type[BaseModel]):
    """
    Convert database documents into a consistent format using a Pydantic model.

    - Converts MongoDB documents (`dict`) into Pydantic model instances
    - Ensures that field names match the expected API response format (including aliasing)
    - Returns a list of serialized Pydantic objects as dictionaries

    :param data: List of MongoDB documents to be normalized
    :param model: Pydantic model class to apply normalization
    :return: List of dictionaries representing the normalized data
    """
    return [model(**doc).dict(by_alias=True) for doc in data]


def check_status_response_for(route: str, model: Type[BaseModel]):
    """
    Test an API route by comparing its response with the expected database data.

    - Sends a GET request to the specified route.
    - Fetches corresponding data from MongoDB using the same route name as the collection name.
    - Normalizes both the database and API response data using the provided Pydantic model.
    - Asserts that the API response matches the expected database data.
    - Ensures that the response status code is 200 (OK).

    :param route: The API endpoint to test (e.g., "/blog", "/book").
    :param model: The Pydantic model corresponding to the expected data structure.
    """
    response = client.get(route)
    cursor = db.process[route].find()

    expected_data = normalize_data(cursor, model)
    response_data = normalize_data(response.json(), model)

    """
    Print both to report
    """
    print("Response data:", response_data)
    print("Expected data:", expected_data)

    assert response_data == expected_data
    assert response.status_code == 200

def check_health(route: str, message: Optional[str] = None):
    """
    Checks the health status of a main API route.

    - Sends a GET request to the specified route.
    - Compares the response status and message.
    - If no message is provided, it defaults to the route name.

    :param route: The API endpoint to test (e.g., "/health").
    :param message: Optional expected status message (defaults to `route` if not provided).
    """
    response = client.get(route)

    print('Response: ', response.status_code)
    expected_message = message if message is not None else route

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": expected_message}
