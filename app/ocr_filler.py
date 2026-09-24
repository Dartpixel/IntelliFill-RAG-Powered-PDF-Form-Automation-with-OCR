import re

import fitz

FONT = "helv"
MIN_FONT_SIZE = 6
UNDERSCORE_RUN = re.compile(r"_{3,}")


def _wrap_text(text, font_size, max_width):
    """Break text into lines that each fit within max_width at font_size."""
    lines = []

    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        current = ""

        for word in words:
            candidate = f"{current} {word}".strip()

            if fitz.get_text_length(candidate, fontname=FONT, fontsize=font_size) <= max_width:
                current = candidate
                continue

            if current:
                lines.append(current)

            # a single word wider than the box still has to go somewhere
            current = word

        lines.append(current)

    return lines


def _layout_text(text, max_width, max_height, font_size):
    """Find the largest font size (>= MIN_FONT_SIZE) whose wrapped lines fit
    within max_height; falls back to the smallest size, clipping lines that
    still don't fit rather than dropping the value entirely."""
    size = font_size

    while size >= MIN_FONT_SIZE:
        line_height = size * 1.3
        lines = _wrap_text(text, size, max_width)

        if len(lines) * line_height <= max_height or size <= MIN_FONT_SIZE:
            max_lines = max(int(max_height // line_height), 1)
            return lines[:max_lines], size, line_height

        size -= 0.5

    line_height = MIN_FONT_SIZE * 1.3
    lines = _wrap_text(text, MIN_FONT_SIZE, max_width)
    max_lines = max(int(max_height // line_height), 1)
    return lines[:max_lines], MIN_FONT_SIZE, line_height


def _field_bounds(page, meta):
    """Compute the (x, y, width, max_bottom) area available for a field's value."""
    x, y, w, _ = meta["bbox"]

    max_bottom = page.rect.height - 10
    next_top = meta.get("next_top")

    if next_top:
        max_bottom = min(max_bottom, next_top - 2)

    return x, y, w, max_bottom


def _find_underline_rects(page, rect):
    """Return rects of any blank-line markers overlapping the field area,
    whether drawn as thin vector line-art or as runs of underscore characters."""
    found = []

    for path in page.get_drawings():
        for item in path.get("items", []):
            if item[0] == "l":
                line_rect = fitz.Rect(item[1], item[2])
            elif item[0] == "re":
                line_rect = fitz.Rect(item[1])
            else:
                continue

            line_rect.normalize()

            is_underline = line_rect.width > line_rect.height * 3 and line_rect.height <= 3

            if is_underline and line_rect.intersects(rect):
                found.append(line_rect)

    for x0, y0, x1, y1, word, *_ in page.get_text("words"):
        if UNDERSCORE_RUN.search(word):
            word_rect = fitz.Rect(x0, y0, x1, y1)

            if word_rect.intersects(rect):
                found.append(word_rect)

    return found


def fill_ocr_pdf(input_pdf_path, output_pdf_path, field_values, fields_metadata):
    """
    Fill a non-AcroForm (OCR-detected) PDF by drawing text at each field's bbox.
    """

    doc = fitz.open(input_pdf_path)

    to_fill = []

    for field_name, value in field_values.items():

        if not value or value == "NOT_FOUND":
            continue

        meta = fields_metadata.get(field_name)

        if not meta or meta.get("type") != "ocr" or not meta.get("bbox"):
            continue

        page_num = meta.get("page", 0)

        if page_num >= len(doc):
            continue

        to_fill.append((value, meta, page_num))

    # Pass 1: erase any underline drawn for the blank, if the template has one
    pages_with_redactions = set()

    for value, meta, page_num in to_fill:
        page = doc[page_num]
        x, y, w, max_bottom = _field_bounds(page, meta)
        rect = fitz.Rect(x, y, x + w, max_bottom)

        for line_rect in _find_underline_rects(page, rect):
            page.add_redact_annot(line_rect, fill=(1, 1, 1))
            pages_with_redactions.add(page_num)

    for page_num in pages_with_redactions:
        doc[page_num].apply_redactions()

    # Pass 2: draw the field values
    for value, meta, page_num in to_fill:
        page = doc[page_num]
        x, y, w, max_bottom = _field_bounds(page, meta)
        font_size = meta.get("font_size", 10)
        max_height = max(max_bottom - y, font_size * 1.3)

        lines, size, line_height = _layout_text(str(value), w, max_height, font_size)

        for i, line in enumerate(lines):
            page.insert_text(
                fitz.Point(x, y + (i + 1) * line_height * 0.85),
                line,
                fontsize=size,
                fontname=FONT,
                color=(0, 0, 0)
            )

    doc.save(output_pdf_path)
    doc.close()

    return output_pdf_path
