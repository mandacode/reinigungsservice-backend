import asyncio
import datetime
import collections
import time

from app.services.google_drive_service import GoogleDriveAsyncService
from app.db.repositories import EmployeeRepository, CustomerRepository, WorkRepository
from app.config import settings
from app.utils import timer, MONTH_MAPPER
from app.domain.engine import generate_invoice


class CustomerInvoiceService:

    def __init__(
            self,
            drive: GoogleDriveAsyncService,
            employee_repository: EmployeeRepository,
            customer_repository: CustomerRepository,
            work_repository: WorkRepository,
    ):
        self._drive = drive
        self._employee_repository = employee_repository
        self._customer_repository = customer_repository
        self._work_repository = work_repository

    @timer
    async def generate_invoices(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            last_invoice_number: str = '1'
    ):
        path = f"customers/{start_date.year}/{start_date.month:02d}"
        s = time.perf_counter()
        tasks = [
            self._drive.create_folder_structure(path),
            self._drive.download(file_id=settings.template_file_id),
            self._employee_repository.get_by_code(code='MJ'),
            self._customer_repository.get_all_with_addresses()
        ]
        folder_id, template, employer, customers = await asyncio.gather(*tasks)
        e = time.perf_counter()
        print(f"Folder created and template downloaded in {e - s:.2f} seconds")

        customers_by_id = {customer.id: customer for customer in customers}

        works = await self._work_repository.get_by_period(
            start_date=start_date,
            end_date=end_date
        )

        customer_works = collections.defaultdict(list)
        for work in works:
            customer_works[work.customer_id].append(work)

        to_upload = []
        for invoice_number, (customer_id, works) in enumerate(customer_works.items(), start=int(last_invoice_number)):

            customer = customers_by_id.get(customer_id)
            total = sum(work.total_price for work in works)

            data = {
                "left_name": customer.name,
                "left_street": customer.address.street_address,
                "left_code": customer.address.postal_code,
                "left_city": customer.address.city,

                "right_name": employer.name,
                "right_company": employer.company_name,
                "right_street": employer.address.street_address,
                "right_code": employer.address.postal_code,
                "right_city": employer.address.city,
                "right_phone": f'Tel.Pl: {employer.metadata.get("contact", {}).get("phone")}',
                "right_email": f'Email: {employer.metadata.get("contact", {}).get("email")}',
                "right_bank_name": employer.bank_account.bank_name,
                "right_iban": employer.bank_account.iban,
                "right_bic": employer.bank_account.bic,
                "right_st_nr": f'St.Nr. {employer.metadata.get("st_nr", "")}',
                "right_ust_id": f'USt-Id.Nr: {employer.metadata.get("vat_id", "")}',

                "invoice_number": invoice_number,
                "date": end_date.strftime('%d.%m.%Y'),
                "year": end_date.year,
                "month": MONTH_MAPPER[end_date.month],
                "extended": customer.metadata.get('extended_invoice', False),

                "note": customer.note,
                "rows": [
                    {
                        "date": work.date.strftime('%d.%m.%Y'),
                        "hours": f"{work.total_hours} Std",
                        "total": f"{work.total_price:.2f} €"
                    }
                    for work in customer_works.get(customer.id, [])
                ],
                "netto": f"{total:.2f} €",
                "tax": f"{total * 0.19:.2f} €",
                "brutto": f"{total * 1.19:.2f} €"
            }

            content = generate_invoice(template=template, data=data)

            filename = self._create_filename(customer.name)
            to_upload.append((content, filename))

        await asyncio.gather(
            *[self.upload_invoice(content, filename, folder_id) for content, filename in to_upload]
        )

    async def upload_invoice(self, content: bytes, filename: str, folder_id: str):
        file_id = await self._drive.upload(
            content=content,
            filename=filename,
            parent_folder_id=folder_id
        )
        print(f"Invoice {filename} uploaded with ID: {file_id}")

        await self._drive.convert_docx_to_pdf(
            file_id=file_id,
            filename=filename,
            folder_id=folder_id
        )
        print(f"Invoice {filename} converted to PDF and saved.")

    @staticmethod
    def _create_filename(name: str) -> str:
        customer_name = (
            name
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )
        return f'{customer_name}.docx'


# TODO 5. Save copy to S3
# TODO 6. Save invoice to database
# TODO 8. Run it asynchronously in background task fastapi
# FIXME update file