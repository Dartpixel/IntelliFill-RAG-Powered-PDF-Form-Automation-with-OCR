from app.auto_fill import generate_form_data

pdf_path = "C:\\Users\\kartik.sharma10137\\intelligent-pdf-autofiller\\data\\uploads\\Single_Line_Form.pdf"

fields, results = generate_form_data(pdf_path)

print()

for field, value in results.items():

    print("=" * 50)
    print(field)
    print(value)