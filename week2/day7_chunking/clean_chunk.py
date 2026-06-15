import re
from pathlib import Path


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def chunk_by_chars(text, chunk_size=300, overlap=50):
    text = clean_text(text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


def chunk_by_paragraphs(text, max_chars=300, min_chars=15):
    text = clean_text(text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 1 <= max_chars:
            current = f"{current}\n{para}".strip()
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return [c for c in chunks if len(c) >= min_chars]


def to_records(chunks, source):
    return [
        {"id": f"{source}#chunk-{i}", "source": source, "text": chunk}
        for i, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":
    raw = """BAO   CAO DON HANG


    Ky bao cao: Thang 06/2026

    Tai lieu nay tom tat cac don hang trong ky.
    He thong OCR se trich xuat noi dung va bang du lieu.



    Cac don hang da duoc xu ly. Lien he: support@company.vn
    """

    print("=== TEXT SAU KHI LÀM SẠCH ===")
    print(clean_text(raw))
    print()

    chunks = chunk_by_paragraphs(raw, max_chars=120)
    print(f"=== CHIA THÀNH {len(chunks)} CHUNK (theo đoạn) ===")
    for record in to_records(chunks, source="report.pdf"):
        print(f"[{record['id']}] ({len(record['text'])} ký tự)")
        print(record["text"])
        print()
