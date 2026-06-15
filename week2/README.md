# Tuần 2: AI Architecture + OCR

Mục tiêu chung của tuần: hiểu toàn bộ kiến trúc hệ thống AI trước khi đi vào chi tiết, và xây được một pipeline OCR hoàn chỉnh — trích xuất text từ ảnh và PDF, tiền xử lý ảnh để tăng độ chính xác, làm sạch và chia chunk để sẵn sàng đưa vào hệ thống RAG ở Tuần 3.

## Bức tranh tổng thể

Tuần 2 là cầu nối: Tuần 1 cho ta nền tảng Python (đọc file, xử lý dữ liệu, gọi API); Tuần 2 dùng nền tảng đó để biến **tài liệu thật (ảnh/PDF) → text sạch → các chunk có cấu trúc**. Đầu ra của tuần này (`output/*_chunks.json`) chính là đầu vào cho bước embedding + vector DB ở Tuần 3.

```
Ảnh / PDF  →  [Trích xuất: OCR hoặc pdfplumber]  →  text thô
           →  [Tiền xử lý ảnh nếu cần]           →  text tốt hơn
           →  [Làm sạch + chunk]                 →  output/<tên>_chunks.json
```

## Yêu cầu hệ thống (cài ngoài Python)

OCR và xử lý PDF cần một số công cụ hệ thống, cài bằng Homebrew trên macOS:

```bash
brew install tesseract tesseract-lang poppler
```

| Công cụ | Vai trò | Kiểm tra |
|---------|---------|----------|
| `tesseract` | Engine OCR chính | `tesseract --version` |
| `tesseract-lang` | Gói ngôn ngữ (có `vie`, `eng`) | `tesseract --list-langs` |
| `poppler` | Cần cho `pdf2image` chuyển PDF → ảnh | `which pdftoppm` |

## Cài đặt môi trường Python

```bash
cd week2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sau khi cài, sinh dữ liệu mẫu để chạy thử (ảnh hóa đơn, ảnh nghiêng/nhiễu, PDF có bảng):

```bash
python make_samples.py                  # tạo ảnh mẫu trong data/samples/
python day5_6_pdf/make_sample_pdf.py    # tạo PDF mẫu data/samples/report.pdf
```

> **Lưu ý về `easyocr`:** thư viện này kéo theo PyTorch (~vài trăm MB) và tải model về máy ở lần chạy đầu tiên (cần mạng). Nếu chỉ cần Tesseract, có thể bỏ dòng `easyocr` trong `requirements.txt`.

## Cách chạy

Mỗi file là một bài học chạy ở terminal, in kết quả ra màn hình:

```bash
python day2_3_basic_ocr/01_tesseract_basic.py
```

Quan trọng: luôn dùng `.venv` của **week2** (vì `pytesseract`, `opencv`… chỉ cài ở đây, không có trong week1).

## Lộ trình & đánh giá theo từng bài

Mỗi bài gồm 3 phần: **Mục tiêu** (học được gì), **Phương thức** (làm thế nào), **Đánh giá kết quả** (tự kiểm tra đã đạt chưa).

### Day 1 — Kiến trúc hệ thống (`day1_architecture/`)

`architecture.py`
- **Mục tiêu:** hiểu kiến trúc AI Chatbot theo mô hình C4 Container — gồm những thành phần nào, dùng công nghệ gì, dữ liệu chảy ra sao.
- **Phương thức:** mô tả 6 container (Chat UI, API Gateway, OCR Pipeline, Vector DB, Query Engine, LLM) bằng `dataclass`; in ra luồng nạp tài liệu (ingest) và luồng hỏi đáp (query).
- **Đánh giá:** vẽ lại được sơ đồ và giải thích vai trò từng container; nói được dữ liệu đi từ "upload tài liệu" đến "sinh câu trả lời" qua những bước nào.
- **Deliverable kèm theo:** sơ đồ `diagrams.png` (vẽ bằng draw.io/tương tự) — đây là phần SA diagram phải demo.

### Day 2–3 — OCR cơ bản (`day2_3_basic_ocr/`)

Cần ảnh mẫu trong `data/samples/` (chạy `make_samples.py` trước).

`01_tesseract_basic.py`
- **Mục tiêu:** dùng Tesseract qua `pytesseract` để trích text từ ảnh; hỗ trợ đa ngôn ngữ (Việt + Anh).
- **Phương thức:** mở ảnh bằng Pillow, gọi `pytesseract.image_to_string(image, lang="vie+eng")`.
- **Đánh giá:** OCR ra đúng nội dung ảnh tiếng Anh và hóa đơn tiếng Việt; biết cách đổi `lang` để đọc ngôn ngữ khác.

`02_ocr_data.py`
- **Mục tiêu:** lấy thông tin chi tiết hơn text — từng từ kèm **độ tin cậy** (confidence %).
- **Phương thức:** dùng `pytesseract.image_to_data(..., output_type=Output.DICT)`, lọc các từ theo ngưỡng `min_conf`, tính độ tin cậy trung bình.
- **Đánh giá:** giải thích được vì sao cần confidence (lọc từ đọc sai, đánh giá chất lượng ảnh); lọc bỏ được các từ có độ tin cậy thấp.

`03_easyocr_demo.py`
- **Mục tiêu:** dùng EasyOCR như một engine thay thế Tesseract (dựa trên deep learning).
- **Phương thức:** tạo `easyocr.Reader(["vi", "en"], gpu=False)`, gọi `readtext()`, lọc theo confidence.
- **Đánh giá:** so sánh được kết quả/độ tin cậy giữa EasyOCR và Tesseract trên cùng ảnh; biết khi nào nên dùng engine nào.

### Day 4 — Tiền xử lý ảnh (`day4_preprocessing/`)

`preprocess.py`
- **Mục tiêu:** cải thiện ảnh trước khi OCR — ảnh sạch hơn thì OCR chính xác hơn.
- **Phương thức:** dùng OpenCV qua 4 bước: `grayscale` (xám hóa) → `denoise` (khử nhiễu) → `deskew` (xoay thẳng) → `threshold` (nhị phân hóa thích nghi). Lưu ảnh từng bước để quan sát.
- **Đánh giá:** giải thích được mỗi bước làm gì; xem được ảnh trung gian trong `output/preprocess/`.

`compare_ocr.py`
- **Mục tiêu:** chứng minh tiền xử lý có ích bằng cách so OCR **trước** và **sau**.
- **Phương thức:** OCR ảnh gốc (nghiêng + nhiễu), rồi OCR ảnh đã qua `full_pipeline`, in cả hai để so sánh.
- **Đánh giá:** thấy rõ kết quả sau xử lý đọc tốt hơn ảnh gốc; hiểu rằng tiền xử lý chỉ hữu ích với ảnh xấu (ảnh đã sạch có thể không cần).

### Day 5–6 — Xử lý PDF (`day5_6_pdf/`)

`make_sample_pdf.py`
- **Mục tiêu:** tạo file PDF mẫu (2 trang, có bảng) để thực hành.
- **Phương thức:** dùng PyMuPDF (`fitz`) vẽ text và bảng, lưu `data/samples/report.pdf`.
- **Đánh giá:** sinh được PDF mẫu để các bài sau dùng.

`01_pdfplumber_text.py`
- **Mục tiêu:** trích text và **bảng** từ PDF dạng text (PDF "thật", không phải ảnh scan).
- **Phương thức:** `pdfplumber.open(...)`, lặp qua từng trang gọi `extract_text()` và `extract_tables()`.
- **Đánh giá:** lấy đúng text cả 2 trang; trích được bảng 4 cột thành list các dòng.

`02_pdf_to_image_ocr.py`
- **Mục tiêu:** xử lý PDF dạng **scan** (mỗi trang là ảnh, không có text) bằng cách chuyển trang → ảnh → OCR.
- **Phương thức:** `pdf2image.convert_from_path()` để render từng trang thành ảnh, rồi OCR từng ảnh bằng `pytesseract`.
- **Đánh giá:** phân biệt được PDF text (dùng pdfplumber) và PDF scan (dùng OCR); chạy được cả hai hướng.

### Day 7 — Làm sạch & chunking (`day7_chunking/`)

`clean_chunk.py`
- **Mục tiêu:** biến text thô (lộn xộn, thừa khoảng trắng) thành các đoạn (chunk) gọn, có cấu trúc, sẵn sàng cho RAG.
- **Phương thức:**
  - `clean_text()` — chuẩn hóa khoảng trắng, xóa dòng trống thừa.
  - `chunk_by_chars()` — chia theo số ký tự, có phần chồng lấp (overlap) giữa các chunk.
  - `chunk_by_paragraphs()` — gộp các đoạn lại tới một giới hạn ký tự, bỏ chunk quá ngắn.
  - `to_records()` — gắn `id` và `source` cho từng chunk (metadata cho vector DB).
- **Đánh giá:** giải thích được vì sao phải chunk (LLM/embedding có giới hạn độ dài) và vì sao cần overlap; tạo ra các chunk có metadata đầy đủ.

## Deliverable cuối tuần (`ocr_pipeline/`)

`pipeline.py` — ghép tất cả lại thành một pipeline OCR hoàn chỉnh:

```bash
python ocr_pipeline/pipeline.py                                # xử lý PDF mẫu
python ocr_pipeline/pipeline.py data/samples/invoice_clean.png # xử lý ảnh
python ocr_pipeline/pipeline.py duong_dan/tai_lieu_that.pdf    # tài liệu của bạn
```

Pipeline tự nhận diện loại file:
- **PDF** → trích text bằng `pdfplumber`.
- **Ảnh** → OCR **cả** bản gốc lẫn bản đã tiền xử lý, rồi chọn kết quả tốt hơn (vì ảnh sạch sẵn thì tiền xử lý đôi khi làm OCR tệ đi).

Sau đó: làm sạch text → chia chunk theo đoạn → gắn `id` + `source` → ghi ra `output/<tên_file>_chunks.json`.

**Tiêu chí hoàn thành tuần:**
1. Sơ đồ SA (kiến trúc) rõ ràng — `diagrams.png` + giải thích được.
2. Pipeline OCR chạy được trên **tài liệu thật** (cả ảnh và PDF), không lỗi.
3. Xuất ra file chunk JSON sạch, mỗi chunk có `id`, `source`, `text` — đúng định dạng để index vào Vector DB ở Tuần 3.

## Cấu trúc thư mục

```
week2/
├── data/samples/          # ảnh & PDF mẫu (sinh bằng script)
├── output/                # kết quả: ảnh tiền xử lý, chunk JSON (tự tạo khi chạy)
├── day1_architecture/     # Day 1 — kiến trúc + diagrams.png
├── day2_3_basic_ocr/      # Day 2–3 — Tesseract, EasyOCR
├── day4_preprocessing/    # Day 4 — tiền xử lý ảnh
├── day5_6_pdf/            # Day 5–6 — xử lý PDF
├── day7_chunking/        # Day 7 — làm sạch & chunk
├── ocr_pipeline/         # Deliverable — pipeline tổng hợp
├── make_samples.py       # sinh ảnh mẫu
└── requirements.txt
```

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `ModuleNotFoundError: No module named 'pytesseract'` | Đang chạy bằng venv của week1 | Dùng `.venv` của week2; hoặc bấm Run sau khi đã cấu hình đúng interpreter |
| `TesseractNotFoundError` | Chưa cài Tesseract hệ thống | `brew install tesseract tesseract-lang` |
| `pdf2image` lỗi không tìm thấy `pdftoppm` | Chưa cài poppler | `brew install poppler` |
| OCR ra rỗng / sai nhiều | Ảnh xấu, nghiêng, nhiễu | Chạy qua `day4_preprocessing` trước khi OCR |
| EasyOCR chạy lần đầu rất lâu | Đang tải model về máy | Chờ tải xong (chỉ lần đầu), cần mạng |
