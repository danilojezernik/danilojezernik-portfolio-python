"""
Routes Overview:
1. POST / - Endpoint for clients to send an email and store it in the database.
2. GET / - Retrieve all emails from the database (private route, requires authentication).
3. GET /{_id} - Retrieve an email by its ID (private route, requires authentication).
4. DELETE /{_id} - Delete an email by its ID (private route, requires authentication).
"""

from fastapi import APIRouter, HTTPException

from src.domain.contact import Contact
from src.services import db, emails
from src.template import email_template

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


@router.post('/', operation_id='client_sent_email_public')
async def client_sent_email_public(emailing: Contact):
    """
    Route for sending an email and storing it in the database.

    Args:
        emailing (Email): The email content provided in the request body.

    Returns:
        dict: A message indicating the status of the email sending and storage.

    Raises:
        HTTPException: If email sending fails or if there's an issue with storing the email data.
        :param request: host
        :param emailing: emails
    """

    # Create the email body using HTML content
    body = email_template.html(full_name=emailing.full_name, message=emailing.message, email=emailing.email)

    # Send the email
    if not emails.send_email(email_from=emailing.email,
                             subject=f'Hypnosis Studio Alen | {emailing.full_name} ti je poslal/a sporočilo ♥',
                             body=body):
        return HTTPException(status_code=500, detail="Email not sent")

    # Store email data in the database
    email_data = {
        "_id": emailing.id,
        "full_name": emailing.full_name,
        "email": emailing.email,
        "message": emailing.message,
        "datum_vnosa": emailing.datum_vnosa
    }
    db.process.email.insert_one(email_data)
    return {"message": "Message was sent"}
