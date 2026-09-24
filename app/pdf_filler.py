from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, BooleanObject, DictionaryObject, NameObject

from app.ocr_filler import fill_ocr_pdf


def get_widget_field_references(writer):
    fields = ArrayObject()

    for page in writer.pages:
        annotations = page.get("/Annots", [])

        for annotation in annotations:
            field = annotation.get_object()

            if field.get("/Subtype") == "/Widget" and field.get("/T"):
                fields.append(annotation)

    return fields


def ensure_acroform_fields(writer, reader):
    acroform = DictionaryObject()
    reader_acroform = reader.trailer["/Root"].get("/AcroForm")

    if reader_acroform:
        for key in ("/DA", "/DR"):
            if key in reader_acroform:
                acroform[NameObject(key)] = reader_acroform[key]

    fields = get_widget_field_references(writer)
    acroform[NameObject("/Fields")] = fields
    acroform[NameObject("/NeedAppearances")] = BooleanObject(True)
    writer._root_object[NameObject("/AcroForm")] = acroform


def fill_pdf(
    input_pdf_path,
    output_pdf_path,
    field_values,
    fields_metadata=None
    ):
    """
    Fill a PDF and save it, dispatching to the OCR filler for
    non-AcroForm PDFs based on the extracted field metadata.
    """

    if fields_metadata and any(
        meta.get("type") == "ocr" for meta in fields_metadata.values()
    ):
        return fill_ocr_pdf(
            input_pdf_path,
            output_pdf_path,
            field_values,
            fields_metadata
        )

    reader = PdfReader(input_pdf_path)

    writer = PdfWriter()

    writer.append_pages_from_reader(reader)

    ensure_acroform_fields(writer, reader)

    # Update values page by page
    # Only update fields if there are values to update
    if field_values:
        for page in writer.pages:
            writer.update_page_form_field_values(
                page,
                field_values
            )

    with open(output_pdf_path, "wb") as output_file:

        writer.write(output_file)

    return output_pdf_path