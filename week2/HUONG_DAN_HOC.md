# 📚 Tài liệu học chi tiết — Tuần 2: AI Architecture + OCR

> Tài liệu này dành cho **người mới hoàn toàn**. Mỗi khái niệm đều được giải thích bằng
> ngôn ngữ đời thường, có ví dụ cụ thể và code thật từ dự án của bạn. Đọc tuần tự từ trên
> xuống, không cần kiến thức trước. Cuối mỗi bài có phần **Câu hỏi & Trả lời** kiểu trainer
> hay hỏi.
>
> 👉 Muốn hiểu **từng dòng code** làm gì? Xem file kèm theo: `PHAN_TICH_CODE.md`.

---

## 0. Trước khi bắt đầu

### 0.1 Tuần 2 này ta làm gì? (Giải thích bằng ví dụ đời thường)

Tưởng tượng bạn có một **chồng hóa đơn giấy** và muốn một con robot đọc hết, hiểu nội dung,
rồi trả lời câu hỏi của bạn như "Tổng tiền hóa đơn tháng 6 là bao nhiêu?".

Để làm được, máy tính phải qua các bước:

1. **Nhìn** vào ảnh/PDF và **đọc chữ** ra (đây là **OCR** — học ở Tuần 2).
2. **Cắt nhỏ** text thành từng đoạn và ghi nhớ (chunking — cuối Tuần 2).
3. **Tìm đoạn liên quan** rồi **trả lời** (RAG — Tuần 3 + 4).

Tuần 2 lo phần 1 và 2: **biến tài liệu (ảnh/PDF) thành text sạch, cắt thành từng mẩu**.

Sơ đồ dòng chảy:

```
  Ảnh / PDF
     │
     ▼
  [Đọc chữ ra]   ← OCR (cho ảnh) hoặc pdfplumber (cho PDF text)
     │
     ▼
  text thô (lộn xộn, có thể sai vài chữ)
     │
     ▼
  [Làm sạch + cắt nhỏ]
     │
     ▼
  output/<tên>_chunks.json   ← đây là sản phẩm cuối tuần, dùng cho Tuần 3
```

### 0.2 OCR là gì? (Khái niệm cốt lõi nhất tuần này)

**OCR = Optical Character Recognition = Nhận dạng ký tự quang học.**

Nói đơn giản: **OCR là công nghệ giúp máy tính "đọc chữ" từ một bức ảnh.**

Ví dụ:
- **Đầu vào:** một bức ảnh chụp tờ giấy có dòng chữ "Hóa đơn 1200 USD".
- **Đầu ra:** chuỗi text `"Hóa đơn 1200 USD"` mà máy tính có thể xử lý, tìm kiếm, tính toán.

Trước khi có OCR, ảnh chỉ là tập hợp các điểm màu — máy tính "thấy" ảnh nhưng không "hiểu"
trong ảnh viết gì. OCR là cây cầu nối từ **hình ảnh** sang **văn bản**.

### 0.3 Cài đặt (làm 1 lần)

Mở Terminal trong VS Code (menu Terminal → New Terminal), gõ lần lượt:

```bash
cd week2
python3 -m venv .venv                 # tạo "môi trường ảo" riêng cho tuần 2
source .venv/bin/activate             # bật nó lên — đầu dòng hiện (.venv) là OK
pip install -r requirements.txt       # cài các thư viện Python
```

Cài thêm 3 công cụ hệ thống (không phải thư viện Python):

```bash
brew install tesseract tesseract-lang poppler
```

- `tesseract` — chương trình OCR (bộ não đọc chữ).
- `tesseract-lang` — gói ngôn ngữ, có tiếng Việt (`vie`) và tiếng Anh (`eng`).
- `poppler` — công cụ để biến trang PDF thành ảnh.

> **Vì sao OCR cần cài cả công cụ hệ thống chứ không chỉ `pip install`?** Vì `pytesseract`
> (thư viện Python) không tự đọc chữ — nó chỉ "ra lệnh" cho chương trình `tesseract` ở máy
> bạn làm việc đó. Không có `tesseract` thì `pytesseract` vô dụng. (Đây chính là lý do lỗi
> `TesseractNotFoundError` mà ta đã gặp.)

Sinh dữ liệu mẫu để có cái mà thực hành:

```bash
python make_samples.py                  # tạo vài ảnh mẫu trong data/samples/
python day5_6_pdf/make_sample_pdf.py    # tạo 1 file PDF mẫu
```

### 0.4 Cách chạy một bài học

```bash
python day2_3_basic_ocr/01_tesseract_basic.py
```

> ⚠️ **Lưu ý quan trọng:** luôn chạy bằng `.venv` của **week2**. Nếu bấm nút ▶ Run mà báo
> `No module named 'pytesseract'` → bạn đang chạy nhầm môi trường của tuần 1. Cách chắc chắn
> nhất là dùng terminal với `(.venv)` ở đầu dòng và đang đứng trong thư mục `week2`.

---

## 1. Day 1 — Kiến trúc hệ thống

📄 File: `day1_architecture/architecture.py` + ảnh `diagrams.png`

### 1.1 Học cái gì? Vì sao học cái này trước?

Trước khi xây nhà, kiến trúc sư vẽ **bản thiết kế** để biết nhà có mấy phòng, phòng nào nối
phòng nào. Phần mềm cũng vậy: trước khi viết code, ta vẽ **sơ đồ kiến trúc** để biết hệ
thống gồm những phần nào, chúng nói chuyện với nhau ra sao.

Sơ đồ của ta vẽ theo **mô hình C4** — một cách vẽ kiến trúc phổ biến, chia làm 4 mức chi
tiết: **C**ontext (bối cảnh) → **C**ontainer (các ứng dụng) → **C**omponent (thành phần) →
**C**ode. Sơ đồ của ta ở mức **Container**: mỗi ô vuông là một ứng dụng/dịch vụ chạy riêng.

### 1.2 Hệ thống AI Chatbot gồm 6 "container"

| # | Container | Công nghệ | Ví như... | Làm gì |
|---|-----------|-----------|-----------|--------|
| 1 | Chat UI | Streamlit | Mặt tiền cửa hàng | Chỗ người dùng gõ câu hỏi, upload file, xem trả lời |
| 2 | API Gateway | FastAPI | Lễ tân | Nhận yêu cầu, điều phối cho các bộ phận khác |
| 3 | OCR Pipeline | Tesseract/EasyOCR | Người đọc tài liệu | Đọc chữ từ ảnh/PDF |
| 4 | Vector DB | ChromaDB | Thư viện có mục lục thông minh | Lưu text và tìm theo ý nghĩa |
| 5 | Query Engine | LangChain | Trợ lý nghiên cứu | Tìm đoạn liên quan, ghép thành câu hỏi đầy đủ |
| 6 | LLM | Gemini/Groq | Chuyên gia trả lời | Đọc ngữ cảnh và viết câu trả lời |

### 1.3 Hai luồng dữ liệu (cực kỳ quan trọng — hay bị hỏi)

**Luồng 1 — Nạp tài liệu (Ingest):** xảy ra khi bạn *upload* file.
```
Upload PDF → API Gateway → OCR đọc chữ → cắt chunk → biến thành vector → lưu vào Vector DB
```

**Luồng 2 — Hỏi đáp (Query):** xảy ra khi bạn *đặt câu hỏi*.
```
Câu hỏi → tìm trong Vector DB các đoạn gần nghĩa nhất → ghép (câu hỏi + đoạn) thành prompt
→ gửi LLM → nhận câu trả lời kèm trích dẫn
```

### 1.4 File `architecture.py` chạy ra gì?

File này dùng `dataclass` (một cách gọn để mô tả "đối tượng có các thuộc tính") để liệt kê
6 container và in ra 2 luồng. Khi chạy:

```
=== CÁC CONTAINER (C4 Container Model) ===
[Streamlit] Chat UI
    -> Nhận câu hỏi và file từ người dùng, hiển thị câu trả lời + citations
[FastAPI] API Gateway
    -> Điều phối: nhận request, gọi OCR pipeline và Query Engine
... (tiếp 4 container nữa)

=== LUỒNG NẠP TÀI LIỆU (Ingest) ===
  1. User upload tài liệu (PDF/ảnh) qua Chat UI
  2. API Gateway nhận file, đẩy sang OCR Pipeline
  ...
```

`diagrams.png` là phiên bản **vẽ trực quan** của cùng nội dung này — dùng để demo.

### ❓ Câu hỏi & Trả lời

**H: Vì sao cần Vector DB mà không lưu vào MySQL/database thường?**
Đ: Vì ta cần tìm theo **ý nghĩa**, không phải khớp từ. Hỏi "giá laptop" phải tìm được đoạn
ghi "máy tính xách tay 1200 USD" dù không có từ "giá". Vector DB lưu text dưới dạng dãy số
(vector) thể hiện ý nghĩa, rồi tìm các đoạn "gần nghĩa" nhất.

**H: LLM là gì?**
Đ: LLM = Large Language Model (mô hình ngôn ngữ lớn) như Gemini, ChatGPT. Nó nhận text vào
và sinh text ra — ở đây là đọc ngữ cảnh ta đưa rồi viết câu trả lời.

**H: OCR chạy ở luồng nào?**
Đ: Chỉ ở **luồng nạp tài liệu** (khi upload). Lúc hỏi đáp không cần OCR nữa vì text đã được
lưu sẵn trong Vector DB.

---

## 2. Day 2–3 — OCR cơ bản

📁 Thư mục: `day2_3_basic_ocr/` (cần chạy `make_samples.py` trước để có ảnh)

### 2.1 `01_tesseract_basic.py` — Đọc chữ từ ảnh

#### Học cái gì?
Dùng Tesseract (qua thư viện `pytesseract`) để biến ảnh → text.

#### Giải thích code dòng quan trọng
```python
image = Image.open(path)                                  # mở file ảnh lên
text = pytesseract.image_to_string(image, lang="vie+eng") # đọc chữ trong ảnh ra text
```
- `Image.open(path)` — dùng thư viện Pillow để mở ảnh (như mở ảnh bằng app xem ảnh).
- `image_to_string` — "đọc toàn bộ chữ trong ảnh và trả về dưới dạng một chuỗi text".
- `lang="vie+eng"` — bảo Tesseract đọc cả tiếng Việt lẫn tiếng Anh. Dấu `+` để ghép nhiều
  ngôn ngữ.

#### Ví dụ thật (ảnh hóa đơn mẫu → text)
**Đầu vào:** ảnh `invoice_clean.png` có chữ.
**Đầu ra khi chạy:**
```
HOA DON BAN HANG
Ma don: 1001
Khach hang: Nguyen Van An
San pham: Laptop Dell XPS
...
```

### ❓ Câu hỏi & Trả lời
**H: `pytesseract` và `tesseract` khác gì nhau?**
Đ: `tesseract` là **chương trình OCR** cài ở máy (qua `brew`). `pytesseract` là **thư viện
Python** chỉ làm cầu nối — nó gọi `tesseract` rồi lấy kết quả về cho Python. Ví như:
`tesseract` là đầu bếp, `pytesseract` là người bồi bàn chuyển order xuống bếp.

**H: OCR đọc sai vài chữ (như "AI" thành "Al") có sao không?**
Đ: Bình thường, vì phụ thuộc chất lượng ảnh. Khắc phục: tiền xử lý ảnh (Day 4) hoặc đổi
engine (EasyOCR).

### 2.2 `02_ocr_data.py` — OCR kèm "độ tin cậy"

#### Học cái gì?
Ngoài text, lấy thêm **độ tin cậy (confidence)** của từng từ — tức OCR "chắc" bao nhiêu % với
mỗi từ nó đọc.

#### Giải thích code
```python
data = pytesseract.image_to_data(image, output_type=Output.DICT)
# data chứa: text từng từ, conf (confidence 0-100), tọa độ từng từ
```
Khác với `image_to_string` (trả text liền), `image_to_data` trả **bảng chi tiết**: mỗi từ
kèm độ tin cậy và vị trí.

#### Ví dụ đầu ra
```
 96%  Training
 99%  Bootcamp
 84%  Email
Độ tin cậy trung bình: 91.2%
```

#### Vì sao hữu ích?
- **Lọc rác:** từ nào tin cậy < 50% thì bỏ, tránh đưa chữ đọc sai vào hệ thống.
- **Chấm điểm ảnh:** trung bình thấp → ảnh xấu → nên tiền xử lý.

### ❓ Câu hỏi & Trả lời
**H: Confidence (độ tin cậy) là gì?**
Đ: Mức "chắc chắn" của OCR với mỗi từ, từ 0 đến 100%. 95% = engine khá chắc từ đó đúng;
20% = nhiều khả năng đọc sai.

### 2.3 `03_easyocr_demo.py` — Một engine khác

#### Học cái gì?
EasyOCR — engine OCR dùng **deep learning** (AI), thường đọc tốt hơn với ảnh khó, chữ nghiêng.

> ⚠️ EasyOCR **nặng**: nó tải mô hình AI về máy ở lần chạy đầu (cần mạng, chờ vài phút).

### ❓ Câu hỏi & Trả lời
**H: Khi nào dùng Tesseract, khi nào EasyOCR?**
Đ: Tesseract — nhanh, nhẹ, tốt với văn bản in rõ. EasyOCR — chính xác hơn với ảnh khó nhưng
chậm và nặng. Tùy tài liệu mà chọn.

---

## 3. Day 4 — Tiền xử lý ảnh (làm ảnh "sạch" trước khi OCR)

📁 Thư mục: `day4_preprocessing/`

### 3.1 Vì sao cần?

OCR giống như mắt người: đọc trang giấy **sạch, thẳng, rõ** thì dễ; đọc trang **mờ, nghiêng,
lem** thì khó và sai. Tiền xử lý = "lau sạch và nắn thẳng" ảnh trước khi đưa cho OCR đọc.

Dùng thư viện **OpenCV** (viết là `cv2` trong code) — thư viện xử lý ảnh mạnh nhất.

### 3.2 Bốn bước trong `preprocess.py`

| Bước | Tên | Giải thích đời thường | Hàm OpenCV |
|------|-----|----------------------|------------|
| 1 | **Grayscale** | Bỏ màu, chỉ giữ đen-trắng-xám (OCR không cần màu) | `cvtColor(..., COLOR_BGR2GRAY)` |
| 2 | **Denoise** | Xóa các đốm nhiễu lấm tấm trên ảnh | `fastNlMeansDenoising` |
| 3 | **Deskew** | Xoay lại ảnh bị nghiêng cho thẳng | `minAreaRect` + `warpAffine` |
| 4 | **Threshold** | Biến ảnh thành chỉ đen/trắng tinh, chữ nổi bật | `adaptiveThreshold` |

### 3.3 `compare_ocr.py` — Chứng minh tiền xử lý có ích

File này chạy OCR **2 lần** trên cùng ảnh nghiêng + nhiễu: một lần ảnh gốc, một lần ảnh đã
xử lý, rồi in cả hai để so. Ví dụ thật:

```
=== TRƯỚC tiền xử lý === ''                                  ← ảnh nghiêng 15°, OCR bó tay
=== SAU tiền xử lý  === 'Preprocessing improves the accuracy ← deskew nắn thẳng → đọc đúng
                         of optical character recognition'
```
→ Từ chỗ **không đọc được gì** thành **đọc đúng hoàn toàn** — đây là minh chứng rõ nhất cho
giá trị của tiền xử lý.

### ❓ Câu hỏi & Trả lời
**H: Vì sao chuyển ảnh sang xám (grayscale)?**
Đ: OCR chỉ quan tâm **hình dạng chữ**, không cần màu sắc. Bỏ màu giúp giảm dữ liệu và làm
các bước sau dễ hơn.

**H: Deskew là gì?**
Đ: Là **xoay ảnh nghiêng về thẳng**. Ảnh chụp/scan thường lệch vài độ; chữ thẳng thì OCR đọc
chuẩn hơn chữ nghiêng.

**H: Threshold (nhị phân hóa) là gì?**
Đ: Biến mỗi điểm ảnh thành **chỉ đen hoặc trắng** dựa trên một ngưỡng sáng/tối. Kết quả: chữ
đen rõ trên nền trắng — lý tưởng cho OCR. "Adaptive" = ngưỡng tự điều chỉnh theo từng vùng,
tốt khi ánh sáng không đều.

**H: Có nên luôn tiền xử lý không?**
Đ: **Không.** Ảnh đã sạch mà ép xử lý có thể làm OCR **tệ hơn**. Vì thế pipeline cuối tuần
thử cả 2 bản (gốc + đã xử lý) rồi chọn bản tốt hơn.

---

## 4. Day 5–6 — Xử lý PDF

📁 Thư mục: `day5_6_pdf/`

### 4.1 Hai loại PDF — phải phân biệt!

| Loại | Là gì | Cách lấy text |
|------|-------|---------------|
| **PDF text** | Xuất từ Word, máy in PDF — chữ là text thật | `pdfplumber` lấy trực tiếp (nhanh, chính xác 100%) |
| **PDF scan** | Chụp/scan trang giấy — mỗi trang là **một bức ảnh** | Phải chuyển trang → ảnh → **OCR** |

Mẹo nhớ: thử bôi đen chữ trong PDF — nếu bôi được (chọn được text) thì là PDF text; không
bôi được (như bôi lên ảnh) thì là PDF scan.

### 4.2 `01_pdfplumber_text.py` — cho PDF text

```python
with pdfplumber.open(path) as pdf:
    for page in pdf.pages:           # duyệt từng trang
        text = page.extract_text()   # lấy chữ
        tables = page.extract_tables()  # lấy bảng (thành list các dòng)
```
`extract_tables()` rất mạnh: nó lấy được **bảng** trong PDF thành list, ví dụ:
```
['Ma don', 'San pham', 'So luong', 'Thanh tien']
['1001', 'Laptop Dell XPS', '1', '1200 USD']
```

### 4.3 `02_pdf_to_image_ocr.py` — cho PDF scan

```python
images = convert_from_path(path, dpi=200)  # biến mỗi trang PDF thành 1 ảnh
for image in images:
    text = pytesseract.image_to_string(image)  # OCR từng ảnh
```
`convert_from_path` thuộc thư viện `pdf2image`, nó cần **poppler** (cài bằng brew) để làm việc.

### ❓ Câu hỏi & Trả lời
**H: Làm sao biết PDF là text hay scan?**
Đ: Thử `extract_text()` của pdfplumber. Ra text → PDF text. Ra rỗng/rất ít → PDF scan, phải OCR.

**H: poppler là gì?**
Đ: Bộ công cụ xử lý PDF ở hệ điều hành. `pdf2image` gọi lệnh `pdftoppm` của poppler để biến
trang PDF thành ảnh. Thiếu nó → lỗi `PDFInfoNotInstalledError`.

**H: Sao không OCR luôn mọi PDF cho gọn?**
Đ: Vì với PDF text, `pdfplumber` cho kết quả **chính xác tuyệt đối và nhanh**, còn OCR có thể
đọc sai. Chỉ OCR khi buộc phải (PDF scan).

---

## 5. Day 7 — Làm sạch & Chunking

📄 File: `day7_chunking/clean_chunk.py`

### 5.1 Chunk là gì? Vì sao phải cắt nhỏ?

**Chunk = một mẩu text nhỏ** được cắt ra từ tài liệu lớn.

Ví dụ: một tài liệu 10 trang được cắt thành ~30 chunk, mỗi chunk vài câu.

Vì sao cắt? Hai lý do:
1. Mô hình AI (embedding) chỉ "nuốt" được đoạn ngắn, không nuốt nổi cả tài liệu dài.
2. Khi tìm kiếm, trả về đúng **đoạn ngắn liên quan** thì chính xác hơn là trả cả tài liệu.

### 5.2 Các hàm trong file

```python
clean_text(text)                       # dọn khoảng trắng thừa, bỏ dòng trống
chunk_by_chars(text, size, overlap)    # cắt theo số ký tự, có phần chồng lấp
chunk_by_paragraphs(text, max_chars)   # gộp các đoạn tới giới hạn, bỏ đoạn quá ngắn
to_records(chunks, source)             # gắn id + nguồn cho mỗi chunk
```

### 5.3 Overlap (chồng lấp) — giải thích bằng hình

Nếu cắt thẳng tay, một câu có thể bị **đứt đôi** giữa 2 chunk → mất ý nghĩa:
```
Chunk 1: "...tổng tiền hóa đơn là"
Chunk 2: "1200 USD chưa gồm thuế..."   ← "là 1200 USD" bị tách rời
```
**Overlap** cho 2 chunk liền nhau chia sẻ vài chục ký tự ở mép, nên ý không bị mất:
```
Chunk 1: "...tổng tiền hóa đơn là 1200 USD"
Chunk 2: "hóa đơn là 1200 USD chưa gồm thuế..."  ← phần "hóa đơn là 1200 USD" lặp lại
```

### 5.4 Mỗi chunk trông như thế nào (đầu ra)
```json
{
  "id": "report.pdf#chunk-0",
  "source": "report.pdf",
  "text": "BAO CAO DON HANG\nKy bao cao: Thang 06/2026"
}
```

### ❓ Câu hỏi & Trả lời
**H: Vì sao mỗi chunk cần `id` và `source`?**
Đ: `source` cho biết chunk đến từ tài liệu nào → để **trích dẫn** trong câu trả lời ("theo
report.pdf..."). `id` để định danh duy nhất khi lưu vào Vector DB.

**H: Cắt theo ký tự hay theo đoạn tốt hơn?**
Đ: Theo đoạn (`chunk_by_paragraphs`) thường tự nhiên hơn vì giữ nguyên ý mỗi đoạn. Theo ký
tự (`chunk_by_chars`) đơn giản, đều đặn, dùng khi text không có cấu trúc đoạn rõ.

---

## 6. Deliverable — Pipeline tổng hợp

📄 File: `ocr_pipeline/pipeline.py`

### 6.1 Làm gì?

Ghép tất cả các bước thành một quy trình tự động: **đưa vào 1 file (ảnh hoặc PDF) → ra 1 file
JSON chứa các chunk sạch.**

```bash
python ocr_pipeline/pipeline.py                                # PDF mẫu
python ocr_pipeline/pipeline.py data/samples/invoice_clean.png # ảnh
python ocr_pipeline/pipeline.py duong_dan/tai_lieu_cua_ban.pdf # tài liệu thật của bạn
```

### 6.2 Pipeline tự quyết định ra sao?

```
File đưa vào
   │
   ├── đuôi .pdf  → dùng pdfplumber lấy text
   │
   └── đuôi ảnh   → OCR cả bản gốc lẫn bản đã tiền xử lý → chọn bản đọc được nhiều chữ hơn
                    │
                    ▼
              làm sạch → cắt chunk → ghi output/<tên>_chunks.json
```

### 6.3 Ví dụ chạy thật
```
Đã xử lý: report.pdf
Độ dài text thô: 381 ký tự
Số chunk tạo ra: 2
Đã ghi: output/report_chunks.json
[report.pdf#chunk-0] BAO CAO DON HANG Ky bao cao: Thang 06/2026...
[report.pdf#chunk-1] Trang 2: Ghi chu Cac don hang tren da duoc xu ly...
```

### ❓ Câu hỏi & Trả lời
**H: Đầu ra pipeline dùng cho gì?**
Đ: File JSON các chunk chính là **đầu vào cho Tuần 3** — sẽ được biến thành vector và lưu vào
Vector DB để chatbot tìm kiếm và trả lời.

**H: Vì sao với ảnh lại OCR 2 lần (gốc + đã xử lý)?**
Đ: Vì không biết trước ảnh sạch hay xấu. Ảnh xấu cần tiền xử lý; ảnh sạch lại bị tiền xử lý
làm hỏng. Chạy cả 2 rồi chọn bản tốt hơn là cách an toàn nhất.

---

## 7. Tự kiểm tra trước khi demo (checklist)

Trả lời trôi chảy 7 câu này nghĩa là bạn đã nắm Tuần 2:

1. ☐ Vẽ + giải thích được sơ đồ kiến trúc (6 container, 2 luồng dữ liệu)?
2. ☐ OCR là gì? `pytesseract` khác `tesseract` ra sao?
3. ☐ Confidence (độ tin cậy) dùng để làm gì?
4. ☐ 4 bước tiền xử lý ảnh là gì, mỗi bước giải quyết vấn đề nào?
5. ☐ Khi nào dùng `pdfplumber`, khi nào phải OCR PDF?
6. ☐ Chunk là gì, vì sao cần overlap và metadata (`id`, `source`)?
7. ☐ Chạy được pipeline trên một tài liệu **thật của bạn** và mở xem file JSON kết quả?

---

## 8. Bảng tra lỗi nhanh

| Lỗi gặp phải | Nguyên nhân | Cách sửa |
|--------------|-------------|----------|
| `No module named 'pytesseract'` | Chạy nhầm venv tuần 1 | Dùng `.venv` của week2 |
| `TesseractNotFoundError` | Chưa cài tesseract / không thấy trong PATH | `brew install tesseract tesseract-lang` |
| `PDFInfoNotInstalledError` | Chưa cài poppler | `brew install poppler` |
| OCR trả về rỗng / sai nhiều | Ảnh xấu, nghiêng, nhiễu | Chạy qua tiền xử lý (Day 4) trước |
| EasyOCR chạy lần đầu rất lâu | Đang tải mô hình AI về máy | Chờ tải xong (chỉ lần đầu), cần mạng |
