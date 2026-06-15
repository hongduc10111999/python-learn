from pathlib import Path

import pdfplumber

PDF_PATH = Path(__file__).parent.parent / "data" / "samples" / "report.pdf"


def extract_text(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


def extract_tables(path):
    tables = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                tables.append(table)
    return tables


if __name__ == "__main__":
    pages = extract_text(PDF_PATH)
    print(f"PDF có {len(pages)} trang\n")
    for i, text in enumerate(pages, 1):
        print(f"--- Trang {i} ---")
        print(text)
        print()

    tables = extract_tables(PDF_PATH)
    print(f"=== Tìm thấy {len(tables)} bảng ===")
    for table in tables:
        for row in table:
            print(row)
