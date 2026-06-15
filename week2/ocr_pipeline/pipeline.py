import json
import sys
from pathlib import Path

import cv2
import pdfplumber
import pytesseract

sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401
from day4_preprocessing.preprocess import full_pipeline
from day7_chunking.clean_chunk import chunk_by_paragraphs, to_records

OUTPUT_DIR = Path(__file__).parent.parent / "output"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def extract_from_image(path, lang="vie+eng"):
    raw_img = cv2.imread(str(path))
    text_raw = pytesseract.image_to_string(raw_img, lang=lang)
    text_pre = pytesseract.image_to_string(full_pipeline(path), lang=lang)
    return text_raw if len(text_raw.strip()) >= len(text_pre.strip()) else text_pre


def extract_from_pdf(path):
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n\n".join(parts)


def run(path, lang="vie+eng"):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".pdf":
        raw = extract_from_pdf(path)
    elif ext in IMAGE_EXTS:
        raw = extract_from_image(path, lang=lang)
    else:
        raise ValueError(f"Định dạng không hỗ trợ: {ext}")

    chunks = chunk_by_paragraphs(raw, max_chars=300)
    records = to_records(chunks, source=path.name)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{path.stem}_chunks.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    return raw, records, out_file


if __name__ == "__main__":
    SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"
    target = sys.argv[1] if len(sys.argv) > 1 else SAMPLE_DIR / "report.pdf"

    raw, records, out_file = run(target)
    print(f"Đã xử lý: {Path(target).name}")
    print(f"Độ dài text thô: {len(raw)} ký tự")
    print(f"Số chunk tạo ra: {len(records)}")
    print(f"Đã ghi: {out_file}\n")
    for r in records:
        print(f"[{r['id']}] {r['text'][:60]}...")
