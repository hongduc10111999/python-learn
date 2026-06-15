# 🔍 Phân tích code chi tiết từng dòng — Tuần 2

> Tài liệu này đi vào **từng dòng code** của mỗi bài học, giải thích cho người mới.
> Đọc kèm với `HUONG_DAN_HOC.md` (phần lý thuyết). Mỗi đoạn code đều có giải thích ngay bên dưới.

**Mục lục**
1. [Day 1 — architecture.py](#day1)
2. [Day 2–3 — 01_tesseract_basic.py](#tess)
3. [Day 2–3 — 02_ocr_data.py](#data)
4. [Day 2–3 — 03_easyocr_demo.py](#easy)
5. [Day 4 — preprocess.py](#prep)
6. [Day 5–6 — 01_pdfplumber_text.py](#pdf)
7. [Day 7 — clean_chunk.py](#chunk)
8. [Deliverable — pipeline.py](#pipe)
9. [Phụ lục — cú pháp Python hay gặp](#phuluc)

---

<a name="day1"></a>
## 1. Day 1 — `day1_architecture/architecture.py`

```python
from dataclasses import dataclass, field
```
Nhập công cụ `dataclass` — cách viết gọn để tạo một "lớp chứa dữ liệu". Thay vì viết hàm
`__init__` dài dòng, ta chỉ cần khai báo các thuộc tính.

```python
@dataclass
class Container:
    name: str
    technology: str
    responsibility: str
```
- `@dataclass` là **decorator** — dán lên trên `class` để Python tự sinh code khởi tạo.
- `Container` mô tả một "container" trong sơ đồ, có 3 thuộc tính: tên, công nghệ, nhiệm vụ.
- `: str` là **gợi ý kiểu** (type hint) — nói rằng các thuộc tính này là chuỗi.

```python
CONTAINERS = [
    Container("Chat UI", "Streamlit", "Nhận câu hỏi và file..."),
    ...
]
```
Tạo một **list** chứa 6 đối tượng `Container`. Mỗi dòng tạo một container với 3 giá trị
truyền vào đúng thứ tự `name, technology, responsibility`.

```python
def print_flow(title, steps):
    print(title)
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print()
```
- Hàm in một "luồng" (danh sách các bước).
- `enumerate(steps, 1)` — duyệt list `steps`, đồng thời đánh số bắt đầu từ 1. Mỗi vòng lặp
  cho ra `i` (số thứ tự) và `step` (nội dung bước).
- `f"  {i}. {step}"` — f-string: chèn giá trị `i` và `step` vào chuỗi.

```python
if __name__ == "__main__":
    for c in CONTAINERS:
        print(f"[{c.technology}] {c.name}")
```
- `if __name__ == "__main__":` — đoạn này chỉ chạy khi ta **chạy trực tiếp** file, không
  chạy khi file bị import bởi file khác.
- `for c in CONTAINERS` — duyệt từng container; `c.technology`, `c.name` truy cập thuộc tính.

---

<a name="tess"></a>
## 2. Day 2–3 — `01_tesseract_basic.py`

```python
import sys
from pathlib import Path
import pytesseract
from PIL import Image
```
- `sys`, `Path` — công cụ thao tác hệ thống và đường dẫn file.
- `pytesseract` — thư viện gọi OCR Tesseract.
- `Image` (từ thư viện Pillow) — để mở và xử lý ảnh.

```python
sys.path.insert(0, str(Path(__file__).parent.parent))
import ocr_config  # noqa: F401
```
- `Path(__file__).parent.parent` — lấy đường dẫn thư mục `week2` (đi lên 2 cấp từ file này).
- `sys.path.insert(0, ...)` — thêm `week2` vào danh sách nơi Python tìm module, để import được
  `ocr_config`.
- `import ocr_config` — nạp file `ocr_config.py`; việc nạp này tự động set đường dẫn tới
  `tesseract` (tránh lỗi `TesseractNotFoundError`). `# noqa: F401` bảo trình kiểm tra "đừng
  cảnh báo import này không dùng" — vì ta dùng *tác dụng phụ* của nó, không dùng tên.

```python
SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"
```
Tạo đường dẫn tới thư mục ảnh mẫu. Dấu `/` ở đây là cách `pathlib` nối đường dẫn (không phải
phép chia). Kết quả: `.../week2/data/samples`.

```python
def ocr_image(path, lang="eng"):
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang=lang)
```
- `lang="eng"` — tham số mặc định: nếu gọi không truyền `lang` thì dùng tiếng Anh.
- `Image.open(path)` — mở file ảnh.
- `image_to_string(...)` — **dòng cốt lõi**: đọc toàn bộ chữ trong ảnh, trả về một chuỗi.

```python
print(ocr_image(note, lang="eng").strip())
```
- Gọi hàm OCR ảnh `note`.
- `.strip()` — cắt bỏ khoảng trắng / dòng trống thừa ở đầu và cuối chuỗi.

---

<a name="data"></a>
## 3. Day 2–3 — `02_ocr_data.py`

```python
from pytesseract import Output
```
Nhập `Output` — dùng để bảo Tesseract trả kết quả ở dạng dictionary (dict).

```python
def words_with_confidence(path, lang="eng", min_conf=0):
    image = Image.open(path)
    data = pytesseract.image_to_data(image, lang=lang, output_type=Output.DICT)
```
- `image_to_data(...)` — khác `image_to_string`: trả về **dữ liệu chi tiết** thay vì text liền.
- `output_type=Output.DICT` — yêu cầu kết quả ở dạng dict. `data` sẽ có các "cột" như
  `data["text"]` (danh sách từ) và `data["conf"]` (danh sách độ tin cậy).

```python
    results = []
    for text, conf in zip(data["text"], data["conf"]):
        conf = int(conf)
        if text.strip() and conf >= min_conf:
            results.append((text, conf))
    return results
```
- `zip(data["text"], data["conf"])` — ghép 2 danh sách lại, mỗi vòng lấy ra một cặp
  `(từ, độ_tin_cậy)` tương ứng.
- `conf = int(conf)` — đổi độ tin cậy sang số nguyên (đôi khi nó là chuỗi).
- `if text.strip() and conf >= min_conf` — chỉ giữ từ **không rỗng** VÀ có độ tin cậy đủ cao.
- `results.append((text, conf))` — thêm cặp vào list kết quả. Dấu `( , )` là một **tuple**.

```python
    avg = sum(c for _, c in words) / len(words)
```
Tính độ tin cậy trung bình. `c for _, c in words` lấy phần `conf` của từng cặp (dấu `_` nghĩa
là "phần text này tôi không dùng đến"). `sum(...) / len(...)` = tổng chia số phần tử.

---

<a name="easy"></a>
## 4. Day 2–3 — `03_easyocr_demo.py`

```python
import warnings
warnings.filterwarnings("ignore")
import easyocr
```
- `warnings.filterwarnings("ignore")` — tắt mọi cảnh báo cho output gọn. Đặt **trước**
  `import easyocr` để chặn cảnh báo phát ra ngay khi nạp thư viện.

```python
reader = easyocr.Reader(["vi", "en"], gpu=False, verbose=False)
```
- Tạo "đầu đọc" EasyOCR cho tiếng Việt (`"vi"`) và tiếng Anh (`"en"`).
- `gpu=False` — chạy bằng CPU (máy không bắt buộc có GPU).
- `verbose=False` — tắt các dòng thông báo EasyOCR tự in (như "Using CPU...").
- Dòng này **chậm** ở lần đầu vì EasyOCR tải mô hình AI về.

```python
def ocr_image(path, min_conf=0.3):
    results = reader.readtext(str(path))
    lines = []
    for box, text, conf in results:
        if conf >= min_conf:
            lines.append((text, conf))
    return lines
```
- `reader.readtext(...)` — đọc ảnh, trả về list, mỗi phần tử gồm 3 thứ:
  `box` (tọa độ khung chữ), `text` (chữ đọc được), `conf` (độ tin cậy, 0–1).
- Vòng lặp lọc giữ những dòng có độ tin cậy ≥ `min_conf` (ở đây 0.3 = 30%).
- Lưu ý: EasyOCR dùng thang **0–1**, còn Tesseract dùng thang **0–100**.

---

<a name="prep"></a>
## 5. Day 4 — `preprocess.py`

```python
import cv2
import numpy as np
```
- `cv2` — thư viện OpenCV, xử lý ảnh.
- `numpy` (viết tắt `np`) — thư viện tính toán trên mảng số; ảnh thực chất là một mảng số.

```python
def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
Chuyển ảnh màu sang ảnh xám. `COLOR_BGR2GRAY` = "từ màu BGR sang Gray". (OpenCV đọc màu theo
thứ tự Blue-Green-Red chứ không phải RGB.)

```python
def denoise(gray):
    return cv2.fastNlMeansDenoising(gray, h=20)
```
Khử nhiễu (xóa đốm lấm tấm). `h=20` là độ mạnh khử nhiễu — số càng lớn xóa càng mạnh nhưng
có thể làm chữ mờ.

```python
def threshold(gray):
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )
```
Nhị phân hóa: biến ảnh xám thành chỉ đen (0) hoặc trắng (255).
- `255` — giá trị gán cho điểm "trắng".
- `ADAPTIVE_THRESH_GAUSSIAN_C` — ngưỡng tính theo từng vùng (thích nghi ánh sáng không đều).
- `THRESH_BINARY` — kiểu nhị phân thường (chữ thành đen, nền trắng).
- `31` — kích thước vùng tính ngưỡng (phải là số lẻ).
- `15` — hằng số trừ đi để tinh chỉnh; tăng lên thì nền sạch hơn.

```python
def _detect_angle(gray):
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                            minLineLength=gray.shape[1] // 3, maxLineGap=20)
    if lines is None:
        return 0.0
    angles = []
    for x1, y1, x2, y2 in lines[:, 0]:
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) <= 45:
            angles.append(angle)
    if not angles:
        return 0.0
    return float(np.median(angles))
```
**Đo góc nghiêng** của ảnh bằng phương pháp Hough Transform (dò đường thẳng):
- `cv2.Canny(...)` — tìm các **cạnh** (đường viền) trong ảnh; dòng chữ tạo thành các cạnh ngang.
- `cv2.HoughLinesP(...)` — dò các **đoạn thẳng** trong ảnh cạnh. `minLineLength=gray.shape[1]//3`
  nghĩa là chỉ nhận đoạn dài ít nhất 1/3 chiều rộng ảnh (để bắt dòng chữ, bỏ nhiễu vụn).
- `if lines is None: return 0.0` — không tìm thấy đường nào thì coi như ảnh thẳng (góc 0).
- `np.arctan2(y2-y1, x2-x1)` — tính góc của mỗi đoạn thẳng; `np.degrees(...)` đổi sang độ.
- `if abs(angle) <= 45` — chỉ giữ các đoạn gần ngang (dòng chữ), bỏ đường dọc.
- `np.median(angles)` — lấy **trung vị** các góc → góc nghiêng tổng thể (trung vị bền với nhiễu
  hơn trung bình).

```python
def deskew(gray):
    angle = _detect_angle(gray)
    if abs(angle) < 0.5:
        return gray
    h, w = gray.shape
    matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(gray, matrix, (w, h),
                          borderMode=cv2.BORDER_REPLICATE, borderValue=255)
```
**Xoay ảnh cho thẳng** dựa trên góc vừa đo:
- `if abs(angle) < 0.5: return gray` — nếu gần thẳng rồi (lệch < 0.5°) thì khỏi xoay, tránh
  làm hỏng ảnh sạch.
- `getRotationMatrix2D((w//2, h//2), angle, 1.0)` — tạo "ma trận xoay" quanh **tâm ảnh** một
  góc `angle` (tỷ lệ 1.0 = giữ nguyên kích thước).
- `warpAffine(...)` — áp dụng phép xoay đó lên ảnh. `borderValue=255` tô nền trắng vào góc
  trống sau khi xoay (255 = trắng).

> 💡 **Vì sao dùng Hough thay vì `minAreaRect`?** `minAreaRect` trả góc theo quy ước riêng của
> OpenCV (khoảng [-90, 0)), rất dễ tính sai dấu/giá trị với ảnh nghiêng nhiều — dẫn tới ảnh
> không được nắn thẳng. Hough dò trực tiếp hướng của dòng chữ nên đo góc chính xác hơn.

```python
def full_pipeline(path, save=False):
    img = cv2.imread(str(path))
    gray = to_grayscale(img)
    clean = denoise(gray)
    straight = deskew(clean)
    binary = threshold(straight)
    ...
    return binary
```
Ghép 4 bước theo thứ tự: đọc ảnh → xám → khử nhiễu → xoay thẳng → nhị phân. Trả về ảnh đã
xử lý xong. `if save:` (nếu truyền `save=True`) thì lưu ảnh từng bước ra file để xem.

---

<a name="pdf"></a>
## 6. Day 5–6 — `01_pdfplumber_text.py`

```python
def extract_text(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages
```
- `with pdfplumber.open(path) as pdf:` — mở file PDF; `with` đảm bảo file tự đóng khi xong.
- `for page in pdf.pages:` — duyệt từng trang.
- `page.extract_text()` — lấy toàn bộ chữ của trang.
- `... or ""` — nếu trang không có chữ (trả `None`) thì dùng chuỗi rỗng `""` thay thế, tránh lỗi.

```python
def extract_tables(path):
    tables = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                tables.append(table)
    return tables
```
- `page.extract_tables()` — tìm các **bảng** trong trang, trả về list các bảng.
- Mỗi `table` là một list các dòng; mỗi dòng là list các ô. Vòng lặp gom tất cả bảng lại.

---

<a name="chunk"></a>
## 7. Day 7 — `clean_chunk.py`

```python
def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()
```
Làm sạch text:
- `replace("\r\n", "\n")` — đồng nhất ký tự xuống dòng (Windows dùng `\r\n`, ta đổi về `\n`).
- `re.sub(r"[ \t]+", " ", text)` — thay nhiều dấu cách/tab liền nhau bằng **một** dấu cách.
  (`re.sub` = tìm theo mẫu rồi thay; `[ \t]+` = một hoặc nhiều dấu cách hoặc tab.)
- `re.sub(r"\n{3,}", "\n\n", text)` — gộp 3+ dòng trống liên tiếp thành 2 (1 dòng trống).
- `[line.strip() for line in text.split("\n")]` — tách thành từng dòng, cắt khoảng trắng mỗi dòng.
- `"\n".join(lines)` — nối các dòng lại bằng ký tự xuống dòng.

```python
def chunk_by_chars(text, chunk_size=300, overlap=50):
    text = clean_text(text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]
```
Cắt theo số ký tự, có chồng lấp:
- `start`, `end` — vị trí đầu và cuối của mẩu cắt hiện tại.
- `text[start:end]` — lấy đoạn từ vị trí `start` đến `end` (gọi là **slicing**).
- `start = end - overlap` — **mấu chốt của overlap**: điểm bắt đầu mẩu tiếp theo lùi lại
  `overlap` ký tự, nên 2 mẩu liền nhau chia sẻ phần đuôi/đầu → không cắt đứt ý.
- `[c for c in chunks if c]` — bỏ các mẩu rỗng.

```python
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
```
Cắt theo đoạn văn (thông minh hơn):
- `text.split("\n\n")` — tách văn bản thành các đoạn (ngăn bởi dòng trống).
- `current` — "giỏ" đang gom các đoạn lại.
- `if len(current) + len(para) + 1 <= max_chars:` — nếu thêm đoạn này vào vẫn chưa vượt giới
  hạn → gộp vào `current`. Ngược lại → "chốt" `current` thành 1 chunk, mở giỏ mới.
- `return [c for c in chunks if len(c) >= min_chars]` — bỏ các chunk quá ngắn (< 15 ký tự).

```python
def to_records(chunks, source):
    return [
        {"id": f"{source}#chunk-{i}", "source": source, "text": chunk}
        for i, chunk in enumerate(chunks)
    ]
```
Gắn metadata cho mỗi chunk:
- Trả về list các **dict**, mỗi dict gồm `id`, `source`, `text`.
- `enumerate(chunks)` — duyệt kèm số thứ tự `i` (0, 1, 2...).
- `f"{source}#chunk-{i}"` — tạo id duy nhất, ví dụ `report.pdf#chunk-0`.

---

<a name="pipe"></a>
## 8. Deliverable — `pipeline.py`

```python
from day4_preprocessing.preprocess import full_pipeline
from day7_chunking.clean_chunk import chunk_by_paragraphs, to_records
```
**Tái sử dụng code**: import lại các hàm đã viết ở Day 4 và Day 7. Đây là điểm hay — không
viết lại, chỉ ghép các mảnh đã có.

```python
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}
```
Một **set** (tập hợp) các đuôi file ảnh, để kiểm tra nhanh "file này có phải ảnh không".

```python
def extract_from_image(path, lang="vie+eng"):
    raw_img = cv2.imread(str(path))
    text_raw = pytesseract.image_to_string(raw_img, lang=lang)
    text_pre = pytesseract.image_to_string(full_pipeline(path), lang=lang)
    return text_raw if len(text_raw.strip()) >= len(text_pre.strip()) else text_pre
```
**Mẹo thông minh nhất của pipeline:**
- `text_raw` — OCR ảnh **gốc**.
- `text_pre` — OCR ảnh **đã tiền xử lý** (gọi `full_pipeline` từ Day 4).
- Dòng cuối: so sánh độ dài 2 kết quả, **chọn bản đọc được nhiều chữ hơn**. Lý do: ảnh sạch
  thì bản gốc tốt hơn, ảnh xấu thì bản tiền xử lý tốt hơn — chọn tự động.
- Cú pháp `A if điều_kiện else B` gọi là **toán tử 3 ngôi**: nếu điều kiện đúng dùng A, sai dùng B.

```python
def extract_from_pdf(path):
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n\n".join(parts)
```
Trích text PDF, nối các trang lại bằng dòng trống (`\n\n`) để phân tách trang.

```python
def run(path, lang="vie+eng"):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".pdf":
        raw = extract_from_pdf(path)
    elif ext in IMAGE_EXTS:
        raw = extract_from_image(path, lang=lang)
    else:
        raise ValueError(f"Định dạng không hỗ trợ: {ext}")
```
**Bộ não điều phối:**
- `path.suffix.lower()` — lấy đuôi file, chuyển thành chữ thường (vd `.PDF` → `.pdf`).
- `if/elif/else` — PDF thì gọi hàm PDF, ảnh thì gọi hàm ảnh, còn lại thì **báo lỗi** rõ ràng.

```python
    chunks = chunk_by_paragraphs(raw, max_chars=300)
    records = to_records(chunks, source=path.name)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{path.stem}_chunks.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
```
- Cắt chunk → gắn metadata (dùng lại hàm Day 7).
- `OUTPUT_DIR.mkdir(parents=True, exist_ok=True)` — tạo thư mục output nếu chưa có (`exist_ok`
  = "đã có thì thôi, đừng báo lỗi").
- `path.stem` — tên file không có đuôi (vd `report.pdf` → `report`).
- `json.dump(...)` — ghi list records ra file JSON. `indent=2` cho dễ đọc; `ensure_ascii=False`
  giữ nguyên tiếng Việt có dấu (nếu `True` sẽ thành `\uXXXX` khó đọc).

---

<a name="phuluc"></a>
## 9. Phụ lục — Cú pháp Python hay gặp trong tuần này

| Cú pháp | Tên gọi | Ý nghĩa | Ví dụ |
|---------|---------|---------|-------|
| `f"...{x}..."` | f-string | Chèn giá trị biến vào chuỗi | `f"Tuổi {age}"` |
| `[x for x in list]` | List comprehension | Tạo list mới từ list cũ | `[n*2 for n in nums]` |
| `[x for x in list if đk]` | Comprehension có lọc | Tạo list, chỉ giữ phần thỏa điều kiện | `[c for c in chunks if c]` |
| `A if đk else B` | Toán tử 3 ngôi | Chọn A hoặc B tùy điều kiện | `x if x > 0 else 0` |
| `with ... as f:` | Context manager | Mở tài nguyên, tự đóng khi xong | `with open(f) as file:` |
| `def f(x, y=0):` | Tham số mặc định | `y` không truyền thì = 0 | `ocr(path, lang="eng")` |
| `for i, x in enumerate(l)` | enumerate | Duyệt kèm số thứ tự | `for i, c in enumerate(chunks)` |
| `zip(a, b)` | zip | Ghép 2 list thành các cặp | `zip(texts, confs)` |
| `path / "sub"` | pathlib | Nối đường dẫn an toàn | `DIR / "data"` |
| `text[a:b]` | Slicing | Lấy đoạn từ vị trí a đến b | `text[0:300]` |
| `_` | Biến bỏ đi | "Giá trị này tôi không dùng" | `for _, c in pairs` |
| `# noqa` | Bỏ qua linter | Bảo trình kiểm tra đừng cảnh báo dòng này | `import x  # noqa` |
