import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_CREDENTIALS_B64 = os.getenv("GOOGLE_API_CREDENTIALS_B64")
SEED_FILE_ID = os.getenv("SEED_FILE_ID")
TEMPLATE_FILE_ID = os.getenv("GOOGLE_DRIVE_CUSTOMERS_TEMPLATE_ID")
GOOGLE_DRIVE_ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")

GOOGLE_DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/drive",
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly'
]
