import sys
from pathlib import Path

import pytesseract
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401

SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"


def ocr_image(path, lang="eng"):
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang=lang)


if __name__ == "__main__":
    print("Phiên bản Tesseract:", pytesseract.get_tesseract_version())
    print("Ngôn ngữ có sẵn:", pytesseract.get_languages())
    print()

    note = SAMPLE_DIR / "note_english.png"
    print(f"=== OCR {note.name} (eng) ===")
    print(ocr_image(note, lang="eng").strip())
    print()

    invoice = SAMPLE_DIR / "invoice_clean.png"
    print(f"=== OCR {invoice.name} (vie+eng) ===")
    print(ocr_image(invoice, lang="vie+eng").strip())
