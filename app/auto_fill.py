from app.form_extractor import extract_form_fields
from app.form_filler import generate_field_value
from app.rag import determine_primary_source


def generate_form_data(pdf_path):

    fields = extract_form_fields(pdf_path)
    print(f"[DEBUG] PDF: {pdf_path}")
    print(f"[DEBUG] Extracted fields: {fields}")
    print(f"[DEBUG] Number of fields: {len(fields)}")

    source = determine_primary_source(list(fields.keys()))
    print(f"[DEBUG] Primary knowledge-base source: {source}")

    results = {}

    for field_name in fields.keys():

        print(
            f"Generating value for: {field_name}"
        )

        value = generate_field_value(
            field_name,
            source=source
        )

        results[field_name] = value

    return fields, results