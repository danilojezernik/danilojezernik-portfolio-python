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

# User in database
USERNAME = str(os.getenv('USERNAME'))
EMAIL = str(os.getenv('EMAIL'))
HASHED_PASSWORD = str(os.getenv('HASHED_PASSWORD'))

