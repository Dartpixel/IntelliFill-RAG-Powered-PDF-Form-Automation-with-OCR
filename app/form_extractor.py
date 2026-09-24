from pypdf import PdfReader

from app.ocr_extractor import extract_ocr_fields


def is_acroform(pdf_path):
    """
    Check if PDF contains form fields
    """

    reader = PdfReader(pdf_path)

    return bool(reader.get_fields()) or bool(extract_widget_fields(reader))


def extract_widget_fields(reader):
    fields = {}

    for page in reader.pages:
        annotations = page.get("/Annots", [])

        for annotation in annotations:
            field = annotation.get_object()

            if field.get("/Subtype") != "/Widget" or not field.get("/T"):
                continue

            field_name = str(field.get("/T"))
            fields[field_name] = {
                "type": field.get("/FT"),
                "value": field.get("/V")
            }

    return fields



def extract_form_fields(pdf_path):

    reader = PdfReader(pdf_path)

    fields = reader.get_fields()

    if not fields:
        widget_fields = extract_widget_fields(reader)

        if widget_fields:
            return widget_fields

        return extract_ocr_fields(pdf_path)

    extracted_fields = {}

    for field_name, field_data in fields.items():

        extracted_fields[field_name] = {
            "type": field_data.get("/FT"),
            "value": field_data.get("/V")
        }

    return extracted_fields