from app.pdf_filler import fill_pdf

field_values = {
    "Project Name": "Nova Inventory Modernization",
    "Project ID": "NIM-2026-047",
    "Client": "Acme Distribution Ltd."
}

fill_pdf(
    input_pdf_path="C:\\Users\\kartik.sharma10137\\intelligent-pdf-autofiller\\data\\knowledge_base\\Space_Exploration_Detailed.pdf",
    output_pdf_path="C:\\Users\\kartik.sharma10137\\intelligent-pdf-autofiller\\data\\uploads\\Single_Line_Form.pdf",
    field_values=field_values
)

print("PDF Generated Successfully")