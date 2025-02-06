import os

from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('PORT'))

# MongoDB connections
DB_MAIN = str(os.getenv('DB_MAIN'))
DB_PROCESS = str(os.getenv('DB_PROCESS'))

# Fast API security
ALGORITHM = str(os.getenv('ALGORITHM'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ROLE_ENCRYPTION_KEY = str(os.getenv('ROLE_ENCRYPTION_KEY'))

# User in database
USERNAME = str(os.getenv('USERNAME'))
EMAIL = str(os.getenv('EMAIL'))
PASSWORD = str(os.getenv('PASSWORD'))
PASSWORD_LOGIN = str(os.getenv('PASSWORD_LOGIN'))

OPENAI_API_KEY = str(os.getenv('OPENAI_API_KEY'))
STACK_URL = str(os.getenv('STACK_URL'))

# GitHub
GITHUB = str(os.getenv('GITHUB'))
GITHUB_TOKEN = str(os.getenv('GITHUB_TOKEN'))

# Newsletter
DOMAIN = str(os.getenv('DOMAIN'))
DOMAIN_REGISTER = str(os.getenv('DOMAIN_REGISTER'))

# TESTING
EMAIL_1 = str(os.getenv('EMAIL_1'))
EMAIL_2 = str(os.getenv('EMAIL_2'))

# TWILIO
ACCOUNT_SID = str(os.getenv('ACCOUNT_SID'))
AUTH_TOKEN = str(os.getenv('AUTH_TOKEN'))
PHONE_NUMBER_TWILIO = str(os.getenv('PHONE_NUMBER_TWILIO'))
PHONE_NUMBER_MY = str(os.getenv('PHONE_NUMBER_MY'))

NGROK = str(os.getenv('NGROK'))
