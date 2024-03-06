import os

from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('PORT'))
DB_MAIN = str(os.getenv('DB_MAIN'))
DB_PROCESS = str(os.getenv('DB_PROCESS'))

