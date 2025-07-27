import base64
import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.utils import timer
from app.config import settings


class GoogleDriveAsyncService:
    @classmethod
    def from_base64(cls, creds_b64: str):
        decoded = base64.b64decode(creds_b64).decode("utf-8")
        service_creds_data = json.loads(decoded)
        return cls(service_creds_data)

    def __init__(self, credentials: dict):
        self._creds = ServiceAccountCreds(
            scopes=settings.google_drive_scopes, **credentials
        )
        self.root_folder_id = settings.google_drive_root_folder_id

    @timer
    async def download(self, file_id: str) -> bytes:
        async with Aiogoogle(service_account_creds=self._creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")

            response = await aiogoogle.as_service_account(
                drive_v3.files.get(fileId=file_id, alt="media"), full_res=True
            )

            return response.content

    @timer
    async def upload(
        self,
        filename: str,
        content: bytes,
        mime_type: str = "application/octet-stream",
        parent_folder_id: str = None,
    ) -> str:
        async with Aiogoogle(service_account_creds=self._creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")

            # File metadata
            metadata = {
                "name": filename,
                "mimeType": mime_type,
                "parents": [parent_folder_id],
            }
            file_id = await self.create_file(
                metadata=metadata, content=content, drive=drive_v3, aiogoogle=aiogoogle
            )
            print(f"File {filename} uploaded successfully. (CREATED)")
            return file_id

    @timer
    async def create_file(
        self, metadata: dict, content: bytes, drive, aiogoogle
    ) -> str:
        file = await aiogoogle.as_service_account(
            drive.files.create(json=metadata, upload_file=content, fields="id")
        )
        return file["id"]

    @timer
    async def update_file(
        self, file_id: str, metadata: dict, content: bytes, drive, aiogoogle
    ) -> str:
        file = await aiogoogle.as_service_account(
            drive.files.update(
                fileId=file_id, json=metadata, upload_file=content, fields="id"
            )
        )
        return file["id"]

    @timer
    async def create_folder_structure(self, name: str) -> str:
        path_parts = name.strip("/").split("/")

        parent_id = self.root_folder_id

        async with Aiogoogle(service_account_creds=self._creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")
            for folder_name in path_parts:
                parent_id = await self._get_or_create_folder(
                    folder_name, parent_id, aiogoogle, drive_v3
                )

        return parent_id

    async def _get_or_create_folder(
        self, folder_name: str, parent_id: str, aig, d
    ) -> str:
        query = (
            f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' "
            f"and '{parent_id}' in parents and trashed = false"
        )

        request = d.files.list(q=query, spaces="drive", fields="files(id, name)")
        results = await aig.as_service_account(request)

        files = results.get("files", [])
        if files:
            return files[0]["id"]

        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }

        folder = await aig.as_service_account(
            d.files.create(json=metadata, fields="id")
        )
        return folder["id"]

    async def convert_docx_to_pdf(self, file_id: str, filename: str, folder_id: str):
        async with Aiogoogle(service_account_creds=self._creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")
            pdf_name = filename.replace(".docx", ".pdf")

            copied_file = await aiogoogle.as_service_account(
                drive_v3.files.copy(
                    fileId=file_id,
                    json={"mimeType": "application/vnd.google-apps.document"},
                )
            )
            copied_file_id = copied_file["id"]

            try:
                pdf_content = await aiogoogle.as_service_account(
                    drive_v3.files.export(
                        fileId=copied_file_id, mimeType="application/pdf"
                    )
                )

                pdf_metadata = {
                    "name": pdf_name,
                    "parents": [folder_id],
                    "mimeType": "application/pdf",
                }
                file_id = await self.create_file(
                    metadata=pdf_metadata,
                    content=pdf_content,
                    drive=drive_v3,
                    aiogoogle=aiogoogle,
                )
                print(f"Converted {filename} to PDF and saved to destination folder")

                return file_id

            finally:
                await aiogoogle.as_service_account(
                    drive_v3.files.delete(fileId=copied_file_id)
                )

    async def get_file_by_name(
        self, filename: str, parent_id: str, aiogoogle, drive_v3
    ) -> dict | None:
        query = f"name='{filename}'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        query += " and trashed=false"

        response = await aiogoogle.as_service_account(
            drive_v3.files.list(q=query, fields="files(id, name, parents)")
        )

        files = response.get("files", [])
        return files[0] if files else None
