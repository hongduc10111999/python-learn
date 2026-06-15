import sys
from pathlib import Path

import cv2
import pytesseract

sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401
from preprocess import full_pipeline

SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"


def ocr(image, lang="eng"):
    return pytesseract.image_to_string(image, lang=lang).strip()


if __name__ == "__main__":
    sample = SAMPLE_DIR / "skewed_noisy.png"

    raw = cv2.imread(str(sample))
    print("=== TRƯỚC tiền xử lý (ảnh gốc nghiêng + nhiễu) ===")
    print(repr(ocr(raw)))
    print()

    processed = full_pipeline(sample)
    print("=== SAU tiền xử lý (deskew + denoise + threshold) ===")
    print(repr(ocr(processed)))
