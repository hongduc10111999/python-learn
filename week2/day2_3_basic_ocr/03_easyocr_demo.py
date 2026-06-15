import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import easyocr

SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"

reader = easyocr.Reader(["vi", "en"], gpu=False, verbose=False)


def ocr_image(path, min_conf=0.3):
    results = reader.readtext(str(path))
    lines = []
    for box, text, conf in results:
        if conf >= min_conf:
            lines.append((text, conf))
    return lines


if __name__ == "__main__":
    target = SAMPLE_DIR / "invoice_clean.png"
    print(f"=== EasyOCR: {target.name} ===")
    for text, conf in ocr_image(target):
        print(f"  {conf:.2f}  {text}")
