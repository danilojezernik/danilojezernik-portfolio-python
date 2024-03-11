from email.message import EmailMessage
import smtplib
from src import env
from src.services import db


def newsletter(subject: str, body: str) -> bool:
    """
    Send a newsletter email to a list of subscribers.

    Args:
        subject (str): The subject of the newsletter email.
        body (str): The HTML content of the newsletter email.

    Returns:
        bool: True if the newsletter email was sent successfully to all subscribers, False otherwise.

    Note:
        This function sends a newsletter email to a list of subscribers without revealing their email addresses to each other.
        It uses the SMTP protocol to send individual emails to each subscriber. Before using this function, make sure to set up
        the Gmail sender email and password in the environment variables 'env.EMAIL_ME' and 'env.EMAIL_PASSWORD'.

    Dependencies:
        - Python's smtplib module for sending emails
    """

    # Retrieve email addresses of subscribers from the database
    cursor = db.process.user.find({}, {'email': 1})
    email_addresses = [document['email'] for document in cursor]

    # Establish an SSL connection to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        for recipient in email_addresses:
            # Create an EmailMessage object for each recipient
            em = EmailMessage()
            em['From'] = env.EMAIL
            em['To'] = recipient
            em['Subject'] = subject
            em.set_content(body, subtype='html')

            # Send the email to the individual recipient
            sendemail = smtp.send_message(em)

            if sendemail:
                return False  # Failed to send the email to at least one recipient

        return True  # Newsletter email sent successfully to all subscribers
