from app.ocr_extractor import extract_ocr_fields
import sys
fields = extract_ocr_fields(r"data\uploads\Space_Template.pdf")
print("NUM_FIELDS:", len(fields), file=sys.stderr)
fields_sorted = sorted(fields, key=lambda f: f["bbox"][1])
for f in fields_sorted:
    print(f["field_name"], f["bbox"], f.get("font_size"), f.get("next_top"))
