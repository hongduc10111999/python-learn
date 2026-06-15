import sys
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path

sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401

PDF_PATH = Path(__file__).parent.parent / "data" / "samples" / "report.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "pdf_pages"


def pdf_to_images(path, dpi=200):
    return convert_from_path(path, dpi=dpi)


def ocr_scanned_pdf(path, lang="eng", dpi=200):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    images = pdf_to_images(path, dpi=dpi)
    results = []
    for i, image in enumerate(images, 1):
        image.save(OUTPUT_DIR / f"page_{i}.png")
        text = pytesseract.image_to_string(image, lang=lang)
        results.append(text.strip())
    return results


if __name__ == "__main__":
    print("Chuyển PDF thành ảnh rồi OCR (dùng khi PDF là bản scan)\n")
    pages = ocr_scanned_pdf(PDF_PATH, lang="vie+eng")
    for i, text in enumerate(pages, 1):
        print(f"--- Trang {i} (OCR) ---")
        print(text)
        print()
    print("Ảnh từng trang đã lưu vào", OUTPUT_DIR)
