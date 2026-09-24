import re

import fitz
import pytesseract
from PIL import Image
from pytesseract import Output

DPI = 300
SCALE = DPI / 72  # PDF points -> pixel scale used for rendering

LABEL_PATTERN = re.compile(r"[A-Za-z][A-Za-z /]*:$")
BLANK_PATTERN = re.compile(r"_{3,}")


def render_pages_to_images(pdf_path, dpi=DPI):
    """Rasterize each PDF page to a PIL image at the given dpi."""
    images = []

    doc = fitz.open(pdf_path)

    matrix = fitz.Matrix(dpi / 72, dpi / 72)

    for page in doc:
        pixmap = page.get_pixmap(matrix=matrix)
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        images.append(image)

    doc.close()

    return images


def ocr_page(image):
    """Run Tesseract OCR and return word-level boxes grouped by line."""
    data = pytesseract.image_to_data(image, output_type=Output.DICT)

    lines = {}

    for i in range(len(data["text"])):
        text = data["text"][i].strip()

        if not text:
            continue

        line_key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])

        word = {
            "text": text,
            "left": data["left"][i],
            "top": data["top"][i],
            "width": data["width"][i],
            "height": data["height"][i],
        }

        lines.setdefault(line_key, []).append(word)

    return lines


def _line_bounds(words):
    left = min(w["left"] for w in words)
    top = min(w["top"] for w in words)
    right = max(w["left"] + w["width"] for w in words)
    bottom = max(w["top"] + w["height"] for w in words)
    return left, top, right, bottom


def _find_value_region(label_end_x, line_top, line_bottom, page_width, page_height, next_line_bounds):
    """Pick the blank region: same line (right of label) vs below the label.

    Tesseract usually fails to OCR long underscore runs as text, so the
    "same line" space can't be measured from detected words alone. Since
    templates typically draw the blank inline after the label, assume the
    row continues to the page margin and only fall back to placing the
    value below the label when there isn't enough width left.
    """
    margin = page_width * 0.05
    same_line_space = (page_width - margin) - label_end_x

    if next_line_bounds:
        below_space = next_line_bounds[1] - line_bottom
    else:
        below_space = min(line_bottom + (line_bottom - line_top) * 2, page_height) - line_bottom

    if same_line_space > 30:
        return (label_end_x, line_top, same_line_space, line_bottom - line_top)

    return (label_end_x, line_bottom, page_width - label_end_x, max(below_space, 1))


def detect_fields_on_page(lines, page_width, page_height):
    fields = {}

    sorted_lines = sorted(lines.items(), key=lambda item: _line_bounds(item[1])[1])

    for idx, (_, words) in enumerate(sorted_lines):
        line_text = " ".join(w["text"] for w in words)

        has_blank = bool(BLANK_PATTERN.search(line_text))
        label_match = LABEL_PATTERN.search(line_text.strip())

        if not label_match and not has_blank:
            continue

        if has_blank:
            blank_word_index = next(
                (i for i, w in enumerate(words) if BLANK_PATTERN.search(w["text"])), None
            )
            label_words = words[:blank_word_index] if blank_word_index else words
        else:
            label_words = words

        field_name = " ".join(w["text"] for w in label_words).rstrip(":").strip()
        field_name = re.sub(r"[^A-Za-z0-9]+", "_", field_name).strip("_")

        if not field_name:
            continue

        left, top, right, bottom = _line_bounds(words)

        next_bounds = None
        if idx + 1 < len(sorted_lines):
            next_bounds = _line_bounds(sorted_lines[idx + 1][1])

        bbox_px = _find_value_region(
            right, top, bottom, page_width, page_height, next_bounds
        )

        # convert pixel bbox -> PDF point space
        bbox_pt = tuple(v / SCALE for v in bbox_px)

        fields[field_name] = {
            "type": "ocr",
            "value": None,
            "bbox": bbox_pt,
            "font_size": max((bottom - top) / SCALE, 8),
            "next_top": next_bounds[1] / SCALE if next_bounds else None,
        }

    return fields


def extract_ocr_fields(pdf_path):
    """Detect form-like fields (label + blank) in a non-AcroForm PDF via OCR."""
    images = render_pages_to_images(pdf_path)

    all_fields = {}

    for page_num, image in enumerate(images):
        lines = ocr_page(image)
        page_fields = detect_fields_on_page(lines, image.width, image.height)

        for field_name, field_data in page_fields.items():
            field_data["page"] = page_num
            all_fields[field_name] = field_data

    return all_fields
