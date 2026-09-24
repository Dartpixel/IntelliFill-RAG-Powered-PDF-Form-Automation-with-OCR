import sys
from pprint import pprint

from app.ocr_extractor import extract_ocr_fields

if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "data/knowledge_base/Space_Exploration_Detailed.pdf"
    fields = extract_ocr_fields(pdf_path)
    print(f"Detected {len(fields)} fields:")
    pprint(fields)
