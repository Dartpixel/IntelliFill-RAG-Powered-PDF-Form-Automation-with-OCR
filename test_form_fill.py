from app.form_filler import generate_field_value

fields = [
    "Project Name",
    "Project ID",
    "Client"
]

for field in fields:

    value = generate_field_value(field)

    print()
    print(field)
    print(value)