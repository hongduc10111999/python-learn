import sys
from pathlib import Path

import pytesseract
from PIL import Image
from pytesseract import Output

sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401

SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"


def words_with_confidence(path, lang="eng", min_conf=0):
    image = Image.open(path)
    data = pytesseract.image_to_data(image, lang=lang, output_type=Output.DICT)
    results = []
    for text, conf in zip(data["text"], data["conf"]):
        conf = int(conf)
        if text.strip() and conf >= min_conf:
            results.append((text, conf))
    return results


if __name__ == "__main__":
    note = SAMPLE_DIR / "note_english.png"
    print(f"=== Từng từ + độ tin cậy: {note.name} ===")
    words = words_with_confidence(note, lang="eng", min_conf=0)
    for text, conf in words:
        print(f"  {conf:3d}%  {text}")

    if words:
        avg = sum(c for _, c in words) / len(words)
        print(f"\nĐộ tin cậy trung bình: {avg:.1f}%")
