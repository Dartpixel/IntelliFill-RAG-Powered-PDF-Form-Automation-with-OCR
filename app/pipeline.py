from app.form_extractor import extract_form_fields
from app.form_filler import generate_field_value
from app.pdf_filler import fill_pdf
from app.rag import determine_primary_source


def process_form(
    input_pdf,
    output_pdf
):

    fields = extract_form_fields(
        input_pdf
    )

    source = determine_primary_source(list(fields.keys()))

    generated_values = {}

    for field_name in fields.keys():

        print(
            f"Generating value for: {field_name}"
        )

        value = generate_field_value(
            field_name,
            source=source
        )

        generated_values[field_name] = value

    print("\nGenerated Values")

    print(generated_values)

    fill_pdf(
        input_pdf_path=input_pdf,
        output_pdf_path=output_pdf,
        field_values=generated_values,
        fields_metadata=fields
    )

    return output_pdf