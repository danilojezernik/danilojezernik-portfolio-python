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


def check_status_response_by_id_for(route: str, model: Type[BaseModel]):
    """
    Test an API route by comparing its response with the expected database data by ID.

    - Fetches the first document from the database for the given collection.
    - Extracts the `_id` and sends a GET request to the API using this ID.
    - Fetches the corresponding document from MongoDB using `find_one()`.
    - Normalizes both the database and API response data using the provided Pydantic model.
    - Asserts that the API response matches the expected database data.
    - Ensures that the response status code is 200 (OK).

    :param route: The API endpoint to test (e.g., "/blog", "/book").
    :param model: The Pydantic model corresponding to the expected data structure.
    """

    # Find the first document in the collection
    first_document = db.process[route].find_one()

    if not first_document:
        print(f"No data found in collection for route: {route}")
        return

    document_id = first_document["_id"]  # Extract the ID

    # Make a request to the API using the extracted ID
    response = client.get(f"{route}/{document_id}")

    # Fetch the expected document using find_one
    expected_data = model(**db.process[route].find_one({"_id": document_id})).dict(by_alias=True)
    response_data = model(**response.json()).dict(by_alias=True)

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


def login_success_helper(monkeypatch, user_name: str, user_password: str):
    """
    Helper function to test a successful login.

    This function performs the following steps:
    1. Defines a DummyUser class whose username attribute is set to `user_name`.
    2. Monkeypatches the `authenticate_user` function in the login module to return an instance of DummyUser
       when the provided credentials match `user_name` and `user_password`. Otherwise, it returns None.
    3. Monkeypatches the `create_access_token` function in the login module to always return "dummy_token".
    4. Sends a POST request to the /login endpoint with the given credentials.
    5. Asserts that the response has a 200 status code and that the JSON response contains the expected
       access token and token type.

    Parameters:
        monkeypatch: The pytest monkeypatch fixture used to override functionality during tests.
        user_name (str): The username to test with.
        user_password (str): The password to test with.
    """
    class DummyUser:
        username = user_name

    monkeypatch.setattr(
        "src.routes.login.authenticate_user",
        lambda username, password: DummyUser() if username == user_name and password == user_password else None
    )

    monkeypatch.setattr(
        "src.routes.login.create_access_token",
        lambda data, expires_delta: "dummy_token"
    )

    response = client.post("/login", data={"username": user_name, "password": user_password})

    assert response.status_code == 200
    json_resp = response.json()
    print(json_resp)
    assert json_resp["access_token"] == "dummy_token"
    assert json_resp["token_type"] == "bearer"


def login_failed_helper(monkeypatch, fake_username: str, fake_password: str):
    """
    Helper function to test a failed login attempt.

    This function performs the following steps:
    1. Monkeypatches the `authenticate_user` function in the login module to always return None, simulating a
       failed authentication scenario.
    2. Sends a POST request to the /login endpoint with fake credentials.
    3. Asserts that the response has a 401 status code and that the JSON response contains the expected
       error message ("Incorrect username or password").

    Parameters:
        monkeypatch: The pytest monkeypatch fixture used to override functionality during tests.
        fake_username (str): The username to test with that should fail authentication.
        fake_password (str): The password to test with that should fail authentication.
    """
    monkeypatch.setattr(
        "src.routes.login.authenticate_user",
        lambda username, password: None
    )

    print('Fake password: ', fake_password)
    print('Fake username: ', fake_username)

    response = client.post("/login", data={"username": fake_username, "password": fake_password})

    assert response.status_code == 401
    json_resp = response.json()
    print(json_resp)
    assert json_resp["detail"] == "Incorrect username or password"
