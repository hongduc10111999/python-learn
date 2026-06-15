from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = Path(__file__).parent / "data" / "samples"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size):
    for path in [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_clean_invoice():
    img = Image.new("RGB", (700, 360), "white")
    draw = ImageDraw.Draw(img)
    title = load_font(34)
    body = load_font(22)
    draw.text((40, 30), "HOA DON BAN HANG", font=title, fill="black")
    lines = [
        "Ma don: 1001",
        "Khach hang: Nguyen Van An",
        "San pham: Laptop Dell XPS",
        "So luong: 1",
        "Don gia: 1200 USD",
        "Tong cong: 1200 USD",
    ]
    for i, line in enumerate(lines):
        draw.text((40, 100 + i * 38), line, font=body, fill="black")
    img.save(SAMPLE_DIR / "invoice_clean.png")


def make_english_note():
    img = Image.new("RGB", (640, 200), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(26)
    draw.text((30, 40), "AI Training Bootcamp 2026", font=font, fill="black")
    draw.text((30, 90), "Week 2: OCR Pipeline", font=font, fill="black")
    draw.text((30, 140), "Email: support@company.vn", font=font, fill="black")
    img.save(SAMPLE_DIR / "note_english.png")


def make_skewed_noisy():
    img = Image.new("RGB", (820, 320), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(38)
    draw.text((60, 60), "Preprocessing improves", font=font, fill="black")
    draw.text((60, 130), "the accuracy of optical", font=font, fill="black")
    draw.text((60, 200), "character recognition", font=font, fill="black")
    img = img.rotate(15, expand=True, fillcolor="white")

    arr = np.array(img).astype(np.int16)
    noise = np.random.default_rng(42).integers(-15, 15, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(SAMPLE_DIR / "skewed_noisy.png")


if __name__ == "__main__":
    make_clean_invoice()
    make_english_note()
    make_skewed_noisy()
    print("Đã tạo ảnh mẫu trong", SAMPLE_DIR)
    for f in sorted(SAMPLE_DIR.glob("*.png")):
        print(" -", f.name)
