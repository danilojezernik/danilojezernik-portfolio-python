from fastapi import APIRouter

from src.domain.user import User
from src.services.security import register_user

router = APIRouter()


@router.post("/", operation_id='register_new_user')
async def register_new_user(user_data: User) -> User:
    """
    Handles user registration by creating a new user and storing the data in the database.

    :param user_data: Registration data containing username, email, full_name, and password.
    :return: The registered user data.
    """

    # Register the user and get the registered user data
    registered_user = register_user(user_data)

    return registered_user
