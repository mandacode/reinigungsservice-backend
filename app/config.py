import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Reinigungsservice"
    debug: bool = False
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")
    admin_key: str = os.getenv("ADMIN_KEY")
    frontend_domain: str = os.getenv("FRONTEND_DOMAIN")
    algorithm: str = "HS256"
    access_token_lifespan: int = 15 * 60  # 15 minutes
    refresh_token_lifespan: int = 1 * 60 * 24  # 1 day
    google_drive_scopes: list[str] = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    google_drive_root_folder_id: str = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    template_file_id: str = os.getenv("GOOGLE_DRIVE_CUSTOMERS_TEMPLATE_ID")
    seed_file_id: str = os.getenv("SEED_FILE_ID")


settings = Settings()
