from fastapi import APIRouter, HTTPException

from src.domain.user import User
from src.services import emails, db
from src.services.security import make_hash
from src.template import registered_user

router = APIRouter()


@router.post("/", operation_id='register_new_user')
async def register_new_user(user_data: User):
    """
    Handles user registration by creating a new user and storing the data in the database.

    :param user_data: Registration data containing username, email, full_name, and password.
    :return: The registered user data.
    """

    # Hash the user's password before storing it
    hashed_password = make_hash(user_data.hashed_password)

    # Create a User object with the provided data
    user_data = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        disabled=False
    )

    # Save the user to the database
    db.process.user.insert_one(user_data.dict(by_alias=True))

    # Generate the HTML body for the email using the provided data
    body = registered_user.html(full_name=user_data.full_name, username=user_data.username, email=user_data.email)

    # Attempt to send the registration email
    if not emails.send_email(email_from=user_data.email, subject='New user registered on danilojezernik.com',
                             body=body):
        # If sending fails, raise an HTTPException with a 500 status code and a detail message
        raise HTTPException(status_code=500, detail='Email not sent')

    # Return a success response
    return {'registered_user'}
