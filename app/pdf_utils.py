import fitz
from pathlib import Path


def read_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def load_knowledge_base(folder_path):
    documents = []

    for pdf_file in Path(folder_path).glob("*.pdf"):

        text = read_pdf(pdf_file)

        documents.append(
            {
                "source": pdf_file.name,
                "content": text
            }
        )

    return documents