import smtplib
from email.message import EmailMessage

from src import env
from src.services import db


def send_email(email_from: str, subject: str, body: str) -> bool:
    """
    Email a specified recipient.

    Args:
        email_from (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The HTML content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Note:
        This function sends an email to a specified recipient using the SMTP protocol to connect to Gmail's SMTP server.
        It's intended for sending individual emails. Before using this function, ensure that you have set up the Gmail
        sender email and password in the environment variables 'env.EMAIL_ME' and 'env.EMAIL_PASSWORD'. Additionally,
        the 'env.EMAIL_ME' should be set to the same Gmail account used for SMTP login.

    Dependencies:
        - Python's smtplib module for sending emails
    """

    # Create an EmailMessage object
    em = EmailMessage()
    em['From'] = email_from
    em['To'] = env.EMAIL
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    # Establish an SSL connection to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        # Send the email from 'env.EMAIL' to 'email_from'
        sendemail = smtp.sendmail(env.EMAIL, env.EMAIL, em.as_string())

        if not sendemail:
            return True
        else:
            return False
