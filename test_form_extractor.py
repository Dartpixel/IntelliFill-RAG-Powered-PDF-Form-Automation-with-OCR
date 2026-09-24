from app.form_extractor import (
    is_acroform,
    extract_form_fields
)

PDF_PATH = "C:\\Users\\kartik.sharma10137\\intelligent-pdf-autofiller\\data\\uploads\\Single_Line_Form.pdf"

print("AcroForm:", is_acroform(PDF_PATH))

print()

fields = extract_form_fields(PDF_PATH)

for field in fields:
    print(field)