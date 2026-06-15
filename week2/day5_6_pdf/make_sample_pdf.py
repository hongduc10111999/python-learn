from pathlib import Path

import fitz

SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def make_pdf():
    doc = fitz.open()
    page = doc.new_page()

    page.insert_text((72, 72), "BAO CAO DON HANG", fontsize=20)
    page.insert_text((72, 110), "Ky bao cao: Thang 06/2026", fontsize=12)

    intro = (
        "Tai lieu nay tom tat cac don hang trong ky. "
        "He thong OCR se trich xuat noi dung va bang du lieu "
        "de phuc vu cho he thong RAG o tuan 3."
    )
    page.insert_textbox(fitz.Rect(72, 140, 520, 220), intro, fontsize=12)

    headers = ["Ma don", "San pham", "So luong", "Thanh tien"]
    rows = [
        ["1001", "Laptop Dell XPS", "1", "1200 USD"],
        ["1002", "Mouse Logitech", "3", "75 USD"],
        ["1003", "Monitor LG 27", "2", "620 USD"],
    ]
    x0, y0, col_w, row_h = 72, 240, 115, 28
    all_rows = [headers] + rows
    for r, row in enumerate(all_rows):
        for c, cell in enumerate(row):
            rect = fitz.Rect(
                x0 + c * col_w, y0 + r * row_h,
                x0 + (c + 1) * col_w, y0 + (r + 1) * row_h,
            )
            page.draw_rect(rect, color=(0, 0, 0), width=0.5)
            page.insert_text((rect.x0 + 4, rect.y0 + 18), cell, fontsize=11)

    page2 = doc.new_page()
    page2.insert_text((72, 72), "Trang 2: Ghi chu", fontsize=16)
    page2.insert_textbox(
        fitz.Rect(72, 100, 520, 200),
        "Cac don hang tren da duoc xu ly. Lien he: support@company.vn",
        fontsize=12,
    )

    out = SAMPLE_DIR / "report.pdf"
    doc.save(out)
    doc.close()
    return out


if __name__ == "__main__":
    out = make_pdf()
    print("Đã tạo PDF mẫu:", out)
