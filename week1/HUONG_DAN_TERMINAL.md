# 🖥️ Hướng dẫn chạy bài học ở Terminal — Week 1 (cho người mới)

> Tài liệu này hướng dẫn **chạy từng file `.py` trực tiếp trên terminal** trong 4 thư mục bài học:
> `day1_2_syntax`, `day3_oop`, `day4_5_data`, `day6_7_api`.
>
> Mỗi bài đều có: **học gì · chạy lệnh nào · kết quả in ra màn hình thế nào · hiểu thế nào**.
> Tất cả kết quả mẫu lấy trực tiếp từ chính code của bạn.

---

## 0. Chuẩn bị (làm 1 lần)

### Terminal là gì?
**Terminal** là cửa sổ dòng lệnh — nơi bạn gõ lệnh để máy tính chạy.
Chạy một file Python nghĩa là gõ: `python <tên_file>.py` rồi Enter.
Mọi thứ chương trình `print(...)` ra sẽ hiện thẳng trên terminal.

### Các bước chuẩn bị
Mở terminal, vào thư mục `week1`:

```bash
cd /Users/doanhongduc/code/learn/python/week1
```

Tạo và kích hoạt **môi trường ảo** (virtual environment — nơi chứa thư viện riêng cho dự án này):

```bash
python3 -m venv .venv          # tạo (đã có sẵn rồi thì bỏ qua)
source .venv/bin/activate      # kích hoạt
pip install -r requirements.txt # cài thư viện (pandas, requests, flask...)
```

✅ Khi kích hoạt thành công, đầu dòng terminal sẽ có chữ `(.venv)`.
Mỗi lần mở terminal mới để học, chỉ cần chạy lại `source .venv/bin/activate`.

### Quy tắc vàng khi chạy bài
> **Luôn đứng ở thư mục `week1`** và gọi file theo đường dẫn đầy đủ, ví dụ:
> ```bash
> python day1_2_syntax/01_variables_types.py
> ```
> *(Riêng `day3_oop/04_imports.py` và `day6_7_api/mini_project` có ngoại lệ — xem phần tương ứng.)*

### Mức độ cần internet
| Nhóm bài | Cần mạng? |
|----------|-----------|
| Day 1–2, Day 3 | ❌ Không |
| Day 4–5 | ❌ Không |
| Day 6–7 (gọi API) | ✅ **Có** |

---

# 📘 DAY 1–2 — Cú pháp Python cơ bản (`day1_2_syntax/`)

---

## Bài 01 — Biến & Kiểu dữ liệu
📄 File: `day1_2_syntax/01_variables_types.py`

```bash
python day1_2_syntax/01_variables_types.py
```

### Học gì
- **Biến**: tên gắn cho một giá trị (`name = "Duc"`).
- **4 kiểu cơ bản**: `str` (chuỗi), `int` (số nguyên), `float` (số thực), `bool` (đúng/sai).
- **f-string**: chèn biến vào chuỗi `f"Xin chào {name}"`.
- **Thao tác chuỗi**: `.lower()`, `.upper()`, `.replace()`, `.split()`, `len()`, kiểm tra `in`.
- **Ép kiểu**: `int("100")` biến chuỗi thành số.
- **Định dạng số**: `f"{price:.1f}"` (1 số lẻ), `f"{price:>10.2f}"` (canh phải, rộng 10 ô).

### Kết quả in ra (tương tự)
```
Duc <class 'str'>
27 <class 'int'>
1.76 <class 'float'>
True <class 'bool'>
Xin chào Duc, năm sau bạn 28 tuổi
ai training bootcamp
AI TRAINING BOOTCAMP
AI Training Course
['AI', 'Training', 'Bootcamp']
20
True
150
Giá: 20.0
Giá:      19.99
```

### Hiểu thế nào
- `type(...)` cho thấy Python **tự nhận biết kiểu** dựa trên cách bạn viết: có nháy `" "` → str, có dấu chấm → float.
- `int("100") + 50 = 150`: phải ép `"100"` thành số trước, vì cộng chuỗi với số sẽ lỗi.
- `{price:.1f}` làm tròn `19.99` thành `20.0`; `{price:>10.2f}` giữ 2 số lẻ và canh lề phải.

---

## Bài 02 — List & Dict
📄 File: `day1_2_syntax/02_lists_dicts.py`

```bash
python day1_2_syntax/02_lists_dicts.py
```

### Học gì
- **List** (`[ ]`): thêm `.append()`, chèn `.insert()`, xóa `.remove()`, cắt lát `fruits[1:3]`, sắp xếp `sorted()`.
- Hàm trên list số: `sum()`, `max()`, `min()`.
- **List comprehension**: `[n*n for n in numbers]`, lọc `[n for n in numbers if n % 2 == 0]`.
- **Dict** (`{ }`): truy cập `["name"]`, an toàn `.get("email", mặc_định)`, sửa/thêm khóa, duyệt `.items()`.
- **Dict comprehension**: lọc dict theo điều kiện.
- **Tuple** (`( )`) và **unpacking**: `x, y = point`.
- **Set** (`{ }` không trùng lặp): tự loại phần tử trùng.

### Kết quả in ra (tương tự)
```
['apple', 'grape', 'orange', 'mango']
apple mango
['grape', 'orange']
['apple', 'grape', 'mango', 'orange']
24 9 1
[25, 4, 81, 1, 49]
[2]
Duc
chưa có email
{'name': 'Duc', 'age': 28, 'skills': ['Python', 'SQL'], 'email': 'hongduc10111999@gmail.com'}
name -> Duc
age -> 28
skills -> ['Python', 'SQL']
email -> hongduc10111999@gmail.com
{'math': 8, 'physics': 9}
10 20
{'python', 'ai', 'ocr'}
```

### Hiểu thế nào
- **List = thứ tự** (lấy bằng vị trí `[0]`); **Dict = tra cứu bằng khóa** (`["name"]`).
- `.get("email", "chưa có email")`: tránh app crash khi khóa chưa tồn tại.
- **Set** in ra `{'python', 'ai', 'ocr'}` — chỉ còn 1 `python` vì set không chứa phần tử trùng (thứ tự có thể khác mỗi lần chạy).

---

## Bài 03 — Hàm (Functions)
📄 File: `day1_2_syntax/03_functions.py`

```bash
python day1_2_syntax/03_functions.py
```

### Học gì
- Định nghĩa hàm `def`, trả về `return`.
- **Tham số mặc định**: `quantity=1`, `discount=0.0`.
- **Trả nhiều giá trị** và **unpack**: `lowest, highest, average = stats([...])`.
- `*args` (nhận nhiều tham số tự do) và `**kwargs` (nhận nhiều tham số có tên).
- **Hàm bậc cao**: truyền một hàm làm tham số cho hàm khác (`apply_twice(add_five, 10)`).

### Kết quả in ra
```
Xin chào Duc!
100.0
300.0
180.0
4 42 18.0
args: (1, 2, 3)
kwargs: {'name': 'Duc', 'course': 'AI Bootcamp'}
20
```

### Hiểu thế nào
- `calc_total(100)` = 100 vì `quantity` mặc định 1, `discount` mặc định 0.
- `calc_total(100, 2, 0.1)` = 100×2×(1−0.1) = **180**.
- `apply_twice(add_five, 10)` = add_five(add_five(10)) = 10+5+5 = **20** → hàm có thể được truyền như dữ liệu.

---

## Bài 04 — Vòng lặp & Lambda
📄 File: `day1_2_syntax/04_loops_lambda.py`

```bash
python day1_2_syntax/04_loops_lambda.py
```

### Học gì
- `for ... in range(...)`: lặp với bước nhảy (`range(1, 10, 2)`).
- `while`: lặp đến khi điều kiện sai (đếm ngược).
- `break` (dừng hẳn) và `continue` (bỏ qua vòng hiện tại).
- `enumerate` (lấy kèm số thứ tự), `zip` (ghép cặp 2 list).
- **lambda**: hàm ngắn 1 dòng. `sorted(..., key=lambda ...)`, `map`, `filter`.

### Kết quả in ra
```
vòng lặp thứ 0
vòng lặp thứ 1
vòng lặp thứ 2
vòng lặp thứ 3
vòng lặp thứ 4
1 3 5 7 9 
đếm ngược: 3
đếm ngược: 2
đếm ngược: 1
0 1 2 4 5 
1 laptop
2 mouse
3 keyboard
laptop: $1000
mouse: $20
keyboard: $50
42
[9, 6, 5, 4, 3, 2, 1, 1]
[{'name': 'Binh', 'age': 22}, {'name': 'Chi', 'age': 27}, {'name': 'An', 'age': 30}]
[6, 2, 8, 2, 10, 18, 4, 12]
[5, 9, 6]
```

### Hiểu thế nào
- Dòng `0 1 2 4 5` — thiếu số 3 (bị `continue` bỏ qua) và dừng trước 6 (`break`).
- `sorted(nums, key=lambda n: -n)` sắp xếp **giảm dần** bằng cách so sánh `-n`.
- `sort(key=lambda p: p["age"])` sắp người theo tuổi tăng dần → Binh(22) → Chi(27) → An(30).

---

# 🧱 DAY 3 — Lập trình hướng đối tượng (`day3_oop/`)

---

## Bài 01 — Class
📄 File: `day3_oop/01_classes.py`

```bash
python day3_oop/01_classes.py
```

### Học gì
- **Class** = khuôn mẫu; **object** = sản phẩm tạo từ khuôn.
- `__init__` (constructor), `self` (chính object đó), **method** (`deposit`/`withdraw`).
- Kiểm tra hợp lệ rồi `raise ValueError` khi sai.
- `__str__`: định dạng object khi in.
- **Biến lớp** `total_created` (dùng chung), `@classmethod`, `@staticmethod`.

### Kết quả in ra
```
Tài khoản của Duc: 600,000 VND
3
Counter đếm số instance đã tạo
```

### Hiểu thế nào
- 500.000 + 200.000 − 100.000 = **600.000** → đúng số dư hiển thị.
- `Counter.how_many()` = 3 vì biến lớp `total_created` **đếm chung** cho cả 3 object đã tạo.
- `__str__` là lý do in `account` ra câu tiếng Việt đẹp thay vì mã object khó đọc.

---

## Bài 02 — Kế thừa (Inheritance)
📄 File: `day3_oop/02_inheritance.py`

```bash
python day3_oop/02_inheritance.py
```

### Học gì
- **Kế thừa**: `Animal` → `Dog`/`Cat` → `Puppy`.
- **Override** (ghi đè method) và `super()` (gọi method lớp cha).
- **Đa hình (polymorphism)**: cùng gọi `.speak()` nhưng mỗi con vật trả khác nhau.
- `isinstance`, `issubclass`.
- `raise NotImplementedError`: ép lớp con phải tự cài đặt method (`Document.extract_text`).

### Kết quả in ra
```
Rex sủa: Gâu gâu!
Mun kêu: Meo meo!
Bun sủa: Gâu gâu! (giọng nhỏ xíu)
Bí ẩn phát ra âm thanh
True
True
Trích xuất text từ PDF: report.pdf
Chạy OCR trên ảnh: scan.png
```

### Hiểu thế nào
- Vòng `for` gọi cùng `.speak()` nhưng kết quả khác nhau → đó là **đa hình**.
- `Puppy` ghép `super().speak()` (lấy của Dog) + `" (giọng nhỏ xíu)"` → tái dùng code cha mà vẫn mở rộng.
- `Document` là **lớp trừu tượng**: gọi trực tiếp sẽ lỗi, buộc `PdfDocument`/`ImageDocument` tự định nghĩa cách trích text.

---

## Bài 03 — Xử lý lỗi (Error Handling)
📄 File: `day3_oop/03_error_handling.py`

```bash
python day3_oop/03_error_handling.py
```

### Học gì
- `try / except / else / finally`:
  - `try`: code có thể lỗi · `except`: bắt từng loại lỗi · `else`: chạy khi KHÔNG lỗi · `finally`: luôn chạy.
- Bắt nhiều loại: `ZeroDivisionError`, `TypeError`, `FileNotFoundError`.
- **Exception tự định nghĩa**: `class InvalidOrderError(Exception)`, dùng `raise` để áp luật nghiệp vụ.

### Kết quả in ra
```
Đã xử lý phép chia 10 / 2
5.0
Không thể chia cho 0
Đã xử lý phép chia 10 / 0
None
Sai kiểu dữ liệu: unsupported operand type(s) for /: 'int' and 'str'
Đã xử lý phép chia 10 / abc
None
Đã xử lý đơn: laptop x2
Lỗi đơn hàng: Đơn hàng thiếu tên sản phẩm
Lỗi đơn hàng: Số lượng phải lớn hơn 0
File không tồn tại, bỏ qua
```

### Hiểu thế nào
- Để ý `finally` ("Đã xử lý phép chia...") **luôn in ra** dù thành công hay lỗi.
- Chia 10/0 và 10/"abc" không làm chương trình sập — lỗi được **bắt** và trả `None`.
- `raise InvalidOrderError(...)` cho phép bạn tự đặt luật: đơn phải có sản phẩm và số lượng > 0.

---

## Bài 04 — Import Module ⚠️ (chạy đặc biệt)
📄 File: `day3_oop/04_imports.py` + `day3_oop/utils/text_tools.py`

> ⚠️ Bài này import module tự viết `utils.text_tools`, nên **phải chạy từ trong thư mục `day3_oop`**:
> ```bash
> cd day3_oop
> python 04_imports.py
> cd ..              # nhớ quay lại week1 sau khi chạy xong
> ```
> Nếu chạy `python day3_oop/04_imports.py` từ `week1` sẽ báo lỗi `ModuleNotFoundError: No module named 'utils'`.

### Học gì
- Import **thư viện chuẩn**: `math`, `datetime` (`date`, `timedelta`), `collections.Counter`.
- Import **module tự viết**: `from utils.text_tools import clean, word_count, truncate`.
- Tách code dùng lại ra file riêng (`text_tools.py`) để gọi từ nhiều nơi.

### Kết quả in ra (ngày sẽ theo hôm bạn chạy)
```
12.0
3.141592653589793
Hôm nay: 2026-06-15
Demo: 2026-06-16
[('python', 3), ('ai', 2)]
AI Training Bootcamp 2026
4
Đây là một câu rất dài...
```

### Hiểu thế nào
- Không cần tự viết căn bậc hai — `math.sqrt(144)=12.0` đã có sẵn. **Lập trình = tận dụng thư viện.**
- `Counter(...).most_common(2)` đếm và trả 2 từ xuất hiện nhiều nhất.
- `truncate(...)` cắt câu dài còn 20 ký tự rồi thêm `...` → đúng kết quả "Đây là một câu rất dài...".

---

# 📊 DAY 4–5 — Xử lý dữ liệu (`day4_5_data/`)

Dữ liệu mẫu nằm trong `day4_5_data/data/` (`orders.csv` có 12 đơn hàng).

---

## Bài 01 — CSV cơ bản (thư viện chuẩn)
📄 File: `day4_5_data/01_csv_basics.py`

```bash
python day4_5_data/01_csv_basics.py
```

### Học gì
- Đọc CSV bằng module chuẩn `csv` + `csv.DictReader` (mỗi dòng thành 1 dict).
- Tính doanh thu, lọc đơn theo danh mục.
- **Ghi ra file CSV mới** bằng `csv.DictWriter`.

### Kết quả in ra
```
Tổng số đơn: 12
Đơn đầu tiên: {'order_id': '1001', 'date': '2026-06-01', 'customer': 'Nguyen Van An', 'product': 'Laptop Dell XPS', 'category': 'Electronics', 'quantity': '1', 'unit_price_usd': '1200'}
Tổng doanh thu: $4,890.00
Số đơn Electronics: 4
Đã ghi file: .../day4_5_data/data/order_totals.csv
```

### Hiểu thế nào
- Bài này **tạo ra file mới** `data/order_totals.csv` — mở file đó để thấy kết quả được lưu lại.
- Khi đọc CSV, mọi giá trị là **chuỗi**, nên phải `int(...)`/`float(...)` trước khi tính toán.

---

## Bài 02 — JSON cơ bản
📄 File: `day4_5_data/02_json_basics.py`

```bash
python day4_5_data/02_json_basics.py
```

### Học gì
- **Ghi JSON ra file**: `json.dump(..., indent=2, ensure_ascii=False)`.
- **Đọc JSON từ file**: `json.load(f)`.
- **Parse chuỗi JSON** → dict: `json.loads(text)`; và ngược lại `json.dumps(...)`.
- Truy cập dữ liệu JSON lồng nhau: `loaded["ocr"]["engine"]`.

### Kết quả in ra
```
Đã ghi: .../day4_5_data/data/config.json
OCR Pipeline
tesseract
['vie', 'eng']
Duc 9.5 True
{"name": "Duc", "score": 9.5, "passed": true}
An: điểm trung bình 7.5
Binh: điểm trung bình 8.5
```

### Hiểu thế nào
- Cặp đối nghịch: **dump/dumps = xuất ra JSON**, **load/loads = đọc JSON vào**.
- `ensure_ascii=False` giúp file giữ nguyên dấu tiếng Việt thay vì mã `\uXXXX`.
- Trong JSON là `true` (thường), khi đọc vào Python thành `True` (hoa).

---

## Bài 03 — Pandas cơ bản
📄 File: `day4_5_data/03_pandas_basics.py`

```bash
python day4_5_data/03_pandas_basics.py
```

### Học gì
- **pandas** = thư viện xử lý bảng dữ liệu (như Excel bằng code).
- `read_csv`, xem nhanh `.head()` / `.info()` / `.describe()`.
- Tạo cột mới, lọc theo điều kiện (`df[df["total_usd"] > 500]`).
- **`groupby().agg()`** — gộp nhóm & tính tổng/đếm/trung bình (giống Pivot Table).
- `nlargest` (top N), `to_csv` (xuất báo cáo).

### Kết quả in ra (rút gọn)
```
   order_id       date  ...  quantity  unit_price_usd
0      1001 2026-06-01  ...         1            1200
...
[in ra .info() và .describe() — thống kê mô tả]
...
             total_revenue  order_count   avg_order
category
Electronics           3869            4  967.250000
Audio                  526            3  175.333333
Accessories            495            5   99.000000
...
Đã ghi: .../day4_5_data/data/category_report.csv
```

### Hiểu thế nào
- `groupby("category").agg(...)` gom đơn cùng danh mục rồi tính tổng/đếm/trung bình → **phân tích dữ liệu cốt lõi**.
- Electronics có các đơn laptop/màn hình giá cao nên doanh thu đứng đầu.
- Bài tạo file `data/category_report.csv` — mở ra để xem báo cáo đã lưu.

---

## Bài 04 — Regex (Biểu thức chính quy)
📄 File: `day4_5_data/04_regex.py`

```bash
python day4_5_data/04_regex.py
```

### Học gì
- **Regex** = mẫu để tìm/trích chuỗi theo quy luật.
- `re.findall` (tìm tất cả), `re.compile` + nhóm có tên `(?P<id>...)`, `re.sub` (thay thế), `re.match` (kiểm tra đầu chuỗi).
- Ký hiệu: `\d` (số), `\w` (chữ/số), `+` (≥1 lần), `{4}` (đúng 4 lần), `\s+` (khoảng trắng).

### Kết quả in ra
```
Emails: ['hongduc10111999@gmail.com', 'support@company.vn']
Phones: ['0912-345-678', '028 3822 9999']
Dates: ['2026-06-01', '2026-06-03']
Prices: ['1,200.00', '75.50']
URLs: ['https://aistudio.google.com', 'https://console.groq.com']
Đơn 1001 đặt ngày 2026-06-01
Đơn 1002 đặt ngày 2026-06-03
... (văn bản với email được thay bằng [EMAIL ĐÃ ẨN]) ...
Hà Nội, Việt Nam
Chuỗi đúng định dạng ngày ISO
```

### Hiểu thế nào
- `\d{4}-\d{2}-\d{2}` = "4 số − 2 số − 2 số" → khớp đúng định dạng ngày.
- `re.sub(email_pattern, "[EMAIL ĐÃ ẨN]", text)` dùng để **che dữ liệu nhạy cảm**.
- `re.sub(r"\s+", " ", messy)` gộp mọi khoảng trắng thừa thành một dấu cách.

---

# 🌐 DAY 6–7 — Gọi API & Dự án nhỏ (`day6_7_api/`)

> ⚠️ **Cần internet** cho tất cả bài trong phần này.

---

## Bài 01 — Gọi REST API
📄 File: `day6_7_api/01_requests_demo.py`

```bash
python day6_7_api/01_requests_demo.py
```

### Học gì
- Gọi API bằng `requests.get(url)`, đọc `.status_code` và `.json()`.
- Truyền tham số: `params={...}`.
- `raise_for_status()` để báo lỗi nếu HTTP thất bại.
- Bắt lỗi mạng: `HTTPError`, `ConnectionError`, `Timeout`.

### Kết quả in ra (dữ liệu thật từ GitHub, số liệu sẽ thay đổi)
```
Status: 200
Tên: Linus Torvalds
Số repo public: 7
Followers: 250000
torvalds/linux - 190,000 sao
... (3 repo Python nhiều sao nhất) ...
Lỗi HTTP: 404
```

### Hiểu thế nào
- `status_code 200` = thành công; `404` = không tìm thấy → đó là lý do dòng cuối in "Lỗi HTTP: 404".
- `.json()` biến phản hồi của server thành dict Python để dễ truy cập.
- Đây là kỹ năng gốc để app của bạn **lấy dữ liệu từ internet**.

---

## Bài cuối tuần — Mini Project (Pipeline dữ liệu) ⚠️ (chạy đặc biệt)
📄 File: `day6_7_api/mini_project/main.py`

> ⚠️ Chạy từ trong thư mục dự án và tạo file `.env` trước:
> ```bash
> cd day6_7_api/mini_project
> cp .env.example .env       # tạo file cấu hình (chỉnh nếu muốn đổi tiền tệ)
> python main.py
> cd ../..                   # quay lại week1
> ```

### Học gì
- Ghép tất cả kỹ năng tuần 1 thành **một pipeline hoàn chỉnh**:
  đọc CSV (pandas) → gọi API tỷ giá (requests) → xử lý → xuất `report.csv` + `summary.json`.
- Đọc cấu hình từ file `.env` bằng `python-dotenv` (không hard-code URL/tiền tệ vào code).
- Ghi nhiều định dạng output (CSV + JSON).

### Kết quả in ra (tỷ giá thật, đổi theo ngày)
```
1. Đọc dữ liệu từ orders.csv
   -> 12 đơn hàng
2. Gọi API lấy tỷ giá USD -> VND
   -> 1 USD = 25,xxx VND
3. Xử lý dữ liệu và tạo báo cáo
4. Xuất báo cáo ra thư mục output

===== TÓM TẮT =====
report_date: 2026-06-15 ...
exchange_rate: {'from': 'USD', 'to': 'VND', 'rate': 25xxx}
total_orders: 12
total_revenue_usd: 4890.0
total_revenue_vnd: 12xxxxxxxx
top_customer: Pham Thi Dao
best_selling_category: Electronics
```

### Hiểu thế nào
- Đây là **deliverable cuối tuần**: chạy end-to-end không lỗi, tạo đủ file trong `output/`.
- Mở 3 file kết quả trong `day6_7_api/mini_project/output/`:
  `report.csv` (chi tiết), `category_report.csv` (theo danh mục), `summary.json` (tóm tắt).
- `.env` cho phép đổi tiền tệ đích mà **không sửa code** — nguyên tắc tách cấu hình khỏi logic.

---

## Demo Web (mở rộng — Streamlit)
📄 File: `day6_7_api/web_demo/app.py`

> Đây là web chứ không phải in ra terminal. Chạy bằng `streamlit` (không phải `python`):
> ```bash
> streamlit run day6_7_api/web_demo/app.py
> ```
> Lệnh sẽ tự mở trình duyệt. Dừng bằng `Ctrl + C`.

### Học gì
- Dựng **dashboard tương tác** chỉ bằng Python (không cần viết HTML/JS).
- Bộ lọc sidebar (`multiselect`, `slider`, `checkbox`), thẻ số liệu (`st.metric`), biểu đồ (`st.bar_chart`, `st.line_chart`).
- `@st.cache_data` để **lưu đệm** kết quả (không gọi API lại liên tục).

### Hiển thị thế nào
- Trình duyệt mở một dashboard "📊 Order Dashboard": lọc danh mục/giá trị đơn, xem doanh thu, biểu đồ theo danh mục & theo ngày, tùy chọn quy đổi VND.

### Hiểu thế nào
- Cùng dữ liệu `orders.csv`, nhưng trình bày trực quan → thấy được sức mạnh khi gắn xử lý dữ liệu với giao diện.

---

# 🎯 Lộ trình & cách học hiệu quả

1. **Day 1–2** (01→04): nền tảng cú pháp — học kỹ, không bỏ qua.
2. **Day 3** (01→04): OOP — cần hiểu Day 1–2 trước.
3. **Day 4–5** (01→04): xử lý dữ liệu thật (CSV/JSON/pandas/regex).
4. **Day 6–7**: gọi API → ráp mini project hoàn chỉnh.

### Mẹo học chủ động
Với mỗi bài, làm theo vòng lặp:
1. **Chạy file** → đọc kết quả trên terminal.
2. **Mở file `.py`** đọc từng dòng, đối chiếu với output.
3. **Sửa một giá trị** (ví dụ đổi `age = 27` thành `age = 30`), lưu, **chạy lại** → xem kết quả đổi thế nào.

Đó là lúc bạn thực sự **hiểu**, không chỉ đọc.

### Bảng tra nhanh lệnh chạy

| Bài | Lệnh (đứng ở `week1`) |
|-----|------------------------|
| Day 1–2 | `python day1_2_syntax/01_variables_types.py` (đổi số file 01→04) |
| Day 3 · 01–03 | `python day3_oop/01_classes.py` (01→03) |
| Day 3 · 04 import | `cd day3_oop && python 04_imports.py && cd ..` |
| Day 4–5 | `python day4_5_data/01_csv_basics.py` (01→04) |
| Day 6–7 · API | `python day6_7_api/01_requests_demo.py` |
| Mini project | `cd day6_7_api/mini_project && cp .env.example .env && python main.py && cd ../..` |
| Web demo | `streamlit run day6_7_api/web_demo/app.py` |

> 📌 Mọi kết quả mẫu ở trên lấy trực tiếp từ code của bạn — chạy thật để đối chiếu 1:1.
