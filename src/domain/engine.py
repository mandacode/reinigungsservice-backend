import io

from docxtpl import DocxTemplate


def generate_invoice(template: bytes, data: dict) -> bytes:
    doc = DocxTemplate(io.BytesIO(template))
    doc.render(context=data)
    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()
