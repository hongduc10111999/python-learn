# 📚 Tài liệu học chi tiết — Week 1 Web App (Python cho người mới)

> Tài liệu này giải thích **từng bài học** trong web app: học cái gì, thao tác ra sao,
> chạy lên hiển thị thế nào, và **hiểu bản chất** như thế nào.
> Đọc theo thứ tự từ trên xuống. Mỗi mục đều có ví dụ chạy thật từ chính code của bạn.

---

## 0. Trước khi bắt đầu — Cách chạy web app

### App này là gì?
Đây là một **web app** nhỏ viết bằng **Flask** (một thư viện Python để làm web).
Nó gồm 2 phần:

- **Backend (Python):** xử lý dữ liệu, tính toán, đọc file CSV, gọi API.
  → Nằm trong [app.py](app.py) và [lessons_basic.py](lessons_basic.py).
- **Frontend (HTML/CSS/JS):** giao diện bạn nhìn thấy trên trình duyệt.
  → Nằm trong thư mục [templates/](templates/).

Luồng hoạt động cơ bản:

```
Trình duyệt  --(gửi yêu cầu URL)-->  Flask (Python)  --(xử lý)-->  trả HTML/JSON  -->  Trình duyệt hiển thị
```

### Các bước chạy

1. Mở terminal, vào thư mục `week1`:
   ```bash
   cd week1
   ```

2. Kích hoạt môi trường ảo (virtual environment) — nơi chứa các thư viện đã cài:
   ```bash
   source .venv/bin/activate
   ```
   Khi thành công, đầu dòng terminal sẽ có chữ `(.venv)`.

3. Vào thư mục web app và chạy:
   ```bash
   cd web_app
   python app.py
   ```

4. Terminal sẽ in ra dòng tương tự:
   ```
   * Running on http://127.0.0.1:5001
   ```

5. Mở trình duyệt, vào địa chỉ: **http://127.0.0.1:5001**

6. Để **dừng** app: bấm `Ctrl + C` trong terminal.

> 💡 App chạy ở chế độ `debug=True` (xem dòng cuối [app.py](app.py#L111)).
> Nghĩa là mỗi khi bạn sửa code Python và lưu lại, app **tự khởi động lại** — không cần tắt/bật tay.

### Bản đồ các trang (URL)

| URL | Trang | Backend xử lý |
|-----|-------|---------------|
| `/` | Trang chủ (danh sách bài) | trả về `index.html` |
| `/lesson/basic/<key>` | Bài cú pháp (chạy code Python) | gọi hàm trong `lessons_basic.py` |
| `/lesson/orders` | Bảng đơn hàng | đọc `orders.csv` bằng pandas |
| `/lesson/stats` | Thống kê doanh thu | pandas `groupby` |
| `/lesson/exchange` | Tỷ giá USD→VND | gọi API tỷ giá qua internet |

---

# PHẦN A — Cú pháp Python cơ bản (Day 1–2)

Các bài này nằm trong [lessons_basic.py](lessons_basic.py).
**Cách hoạt động chung:** Mỗi bài là một **hàm Python**. Khi bạn mở URL `/lesson/basic/<key>`,
Flask gọi hàm đó, hàm trả về một **danh sách các dòng** dạng `(biểu thức, kết quả, kiểu dữ liệu)`,
rồi đổ vào bảng HTML trong [templates/basic.html](templates/basic.html).

Bạn sẽ thấy một **bảng 3 cột**: Biểu thức · Kết quả · Kiểu.

---

## A1 — Biến & Kiểu dữ liệu
📍 URL: `/lesson/basic/variables` · Hàm: `variables_types()` ([lessons_basic.py:1](lessons_basic.py#L1))

### Học gì
- **Biến** (variable): cái tên để lưu một giá trị. Ví dụ `age = 27` nghĩa là "đặt tên `age` cho số 27".
- **Các kiểu dữ liệu cơ bản:**
  - `str` (chuỗi/text): `"Duc"` — luôn có dấu nháy `" "`.
  - `int` (số nguyên): `27`.
  - `float` (số thực có dấu phẩy): `1.76`.
  - `bool` (đúng/sai): `True` / `False`.
- **f-string**: cách chèn biến vào chuỗi: `f"Xin chào {name}"`.
- **Phương thức (method) của chuỗi**: `.upper()` (viết hoa), `.split()` (cắt chuỗi thành list).
- **Ép kiểu (type casting)**: `int("100")` biến chuỗi `"100"` thành số `100`.

### Thao tác
Không cần thao tác gì — chỉ mở URL. Code đã viết sẵn các biến và biểu thức.

### Chạy hiển thị thế nào
Bảng sẽ hiện các dòng như:

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `name` | Duc | str |
| `age` | 27 | int |
| `f-string` | Xin chào Duc, năm sau bạn 28 tuổi | str |
| `text.upper()` | AI TRAINING BOOTCAMP | str |
| `int("100") + 50` | 150 | int |

### Hiểu thế nào
- Cột **Kiểu** là quan trọng nhất: Python phân biệt rõ `"100"` (chuỗi) và `100` (số).
  Nếu cộng `"100" + 50` sẽ **lỗi**, nên phải dùng `int("100")` trước.
- `f"... {age + 1} ..."` cho thấy: trong dấu `{}` bạn có thể **tính toán** chứ không chỉ chèn biến.
- `f"{price:.1f}"` là **định dạng số**: `.1f` = làm tròn 1 chữ số thập phân → `19.99` thành `20.0`.

---

## A2 — List & Dict
📍 URL: `/lesson/basic/lists` · Hàm: `lists_dicts()` ([lessons_basic.py:21](lessons_basic.py#L21))

### Học gì
- **List** (danh sách): nhiều giá trị xếp theo thứ tự, dùng `[ ]`. Ví dụ `["apple", "banana"]`.
  - Lấy phần tử: `fruits[0]` (phần tử đầu), `fruits[-1]` (phần tử cuối).
  - Hàm hữu ích: `sum()`, `max()`, `min()`, `sorted()`.
- **Dict** (từ điển): cặp **khóa → giá trị**, dùng `{ }`. Ví dụ `{"name": "Duc", "age": 27}`.
  - Lấy giá trị: `student["name"]`.
  - An toàn hơn: `student.get("email", "chưa có")` — nếu không có khóa thì trả giá trị mặc định, không lỗi.
- **List comprehension**: cách viết gọn để tạo list mới từ list cũ:
  - `[n * n for n in numbers]` = bình phương mỗi số.
  - `[n for n in numbers if n % 2 == 0]` = chỉ lấy số chẵn (`%` là phép chia lấy dư).

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `fruits đã sort` | ['apple', 'banana', 'mango', 'orange'] | list |
| `sum / max / min` | 24 / 9 / 1 | int |
| `bình phương (comprehension)` | [25, 4, 81, 1, 49] | list |
| `lọc số chẵn` | [2] | list |
| `môn đạt >= 8` | {'math': 8, 'physics': 9} | dict |

### Hiểu thế nào
- **List = thứ tự** (lấy bằng số chỉ mục `[0]`), **Dict = tra cứu bằng tên khóa** (`["name"]`).
- List comprehension đọc như tiếng Anh: "lấy `n*n` **với mỗi** `n` **trong** numbers".
- `{k: v for k, v in scores.items() if v >= 8}` là **dict comprehension**: lọc dict theo điều kiện.
- `.get()` rất hay dùng thực tế để tránh app bị crash khi thiếu dữ liệu.

---

## A3 — Hàm (Functions)
📍 URL: `/lesson/basic/functions` · Hàm: `functions()` ([lessons_basic.py:38](lessons_basic.py#L38))

### Học gì
- **Hàm**: một khối code có tên, nhận **tham số (parameter)** vào và **trả về (return)** kết quả.
  ```python
  def calc_total(price, quantity=1, discount=0.0):
      return price * quantity * (1 - discount)
  ```
- **Tham số mặc định**: `quantity=1` nghĩa là nếu không truyền vào thì mặc định = 1.
- **Tham số theo tên (keyword argument)**: `calc_total(100, quantity=2, discount=0.1)` — rõ ràng hơn.
- **Trả về nhiều giá trị**: `return min, max, average` → nhận bằng `a, b, c = stats(...)`.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `calc_total(100)` | 100.0 | float |
| `calc_total(100, 3)` | 300.0 | float |
| `calc_total(100, 2, 0.1)` | 180.0 | float |
| `stats() -> trung bình` | 18.0 | float |

### Hiểu thế nào
- Cùng một hàm `calc_total` cho ra kết quả khác nhau tùy bạn truyền bao nhiêu tham số → **tái sử dụng code**.
- `calc_total(100)` chỉ truyền 1 tham số nhưng vẫn chạy được vì `quantity` và `discount` có giá trị mặc định.
- `lowest, highest, average = stats([...])` gọi là **unpacking** — "tháo gói" nhiều giá trị trả về cùng lúc.

---

## A4 — Vòng lặp & Lambda
📍 URL: `/lesson/basic/loops` · Hàm: `loops_lambda()` ([lessons_basic.py:56](lessons_basic.py#L56))

### Học gì
- `range(1, 10, 2)` — sinh dãy số từ 1 đến 9, **bước nhảy 2** → `[1, 3, 5, 7, 9]`.
- `enumerate(...)` — vừa lấy phần tử vừa lấy **số thứ tự**.
- `zip(a, b)` — **ghép cặp** hai list: `zip(["laptop"], [1000])` → `[("laptop", 1000)]`.
- **lambda** — hàm ngắn gọn 1 dòng, không cần `def`. Ví dụ `lambda n: -n`.
- `sorted(..., key=lambda p: p["age"])` — sắp xếp theo tiêu chí tùy ý (ở đây: theo tuổi).
- `map()` — áp dụng một hàm lên **mọi** phần tử. `filter()` — **lọc** phần tử thỏa điều kiện.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `range(1, 10, 2)` | [1, 3, 5, 7, 9] | list |
| `zip tên + giá` | [('laptop', 1000), ('mouse', 20), ('keyboard', 50)] | list |
| `sort theo tuổi` | ['Binh', 'Chi', 'An'] | list |
| `map nhân đôi` | [6, 2, 8, ...] | list |
| `filter > 4` | [5, 9, 6] | list |

### Hiểu thế nào
- **lambda** = "hàm dùng một lần". `lambda n: -n` đọc là "nhận `n`, trả về `-n`".
- `key=lambda p: p["age"]` bảo `sorted` rằng: "khi so sánh, hãy nhìn vào trường `age`".
- `map`/`filter` là cách xử lý dữ liệu hàng loạt rất phổ biến (giống list comprehension).

---

# PHẦN B — OOP & Module (Day 3)

OOP = **Lập trình hướng đối tượng** (Object-Oriented Programming).
Ý tưởng: gom dữ liệu + hành vi liên quan vào một **class** (lớp), rồi tạo ra các **object** (đối tượng) từ class đó.

---

## B1 — Class (Lớp)
📍 URL: `/lesson/basic/classes` · Hàm: `oop_classes()` ([lessons_basic.py:77](lessons_basic.py#L77))

### Học gì
- **Class** là "khuôn mẫu". **Object** là sản phẩm tạo ra từ khuôn đó.
  ```python
  class BankAccount:
      def __init__(self, owner, balance=0):  # hàm khởi tạo, chạy khi tạo object
          self.owner = owner                 # self = chính object này
          self.balance = balance
  ```
- `__init__` — **constructor**, tự chạy khi tạo object: `BankAccount("Duc", 500000)`.
- `self` — đại diện cho **chính đối tượng đang xét**. `self.balance` là số dư của riêng tài khoản đó.
- **Method** — hàm bên trong class: `deposit()` (nạp), `withdraw()` (rút).
- `__str__` — quy định object **hiển thị** thành chuỗi thế nào khi in ra.
- **Biến lớp (class variable)**: `total_created` đếm số object đã tạo, **dùng chung** cho cả lớp.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `Tạo BankAccount('Duc', 500000)` | balance = 500,000 | BankAccount |
| `deposit(200000) rồi withdraw(100000)` | Tài khoản của Duc: 600,000 VND | str |
| `Tạo 3 Counter, Counter.how_many()` | 3 | int |

### Hiểu thế nào
- 500.000 + 200.000 (nạp) − 100.000 (rút) = **600.000** → đúng kết quả hiển thị.
- Mỗi object `BankAccount` có số dư **riêng** (lưu trong `self.balance`).
- `Counter.total_created = 3` vì biến lớp **dùng chung**: tạo 3 object thì đếm thành 3.
- `__str__` giải thích vì sao in tài khoản ra lại đẹp như câu tiếng Việt thay vì mã loằng ngoằng.

---

## B2 — Kế thừa (Inheritance)
📍 URL: `/lesson/basic/inheritance` · Hàm: `oop_inheritance()` ([lessons_basic.py:113](lessons_basic.py#L113))

### Học gì
- **Kế thừa**: một class con dùng lại mọi thứ của class cha, có thể **ghi đè (override)**.
  - `Animal` (cha) → `Dog`, `Cat` (con) → `Puppy` (cháu, kế thừa từ `Dog`).
- **Override**: `Dog` viết lại `speak()` để kêu "Gâu gâu" thay vì âm thanh chung.
- `super()` — gọi method của class cha. `Puppy` dùng `super().speak()` rồi thêm chữ.
- `isinstance(obj, Class)` — kiểm tra object có thuộc class đó không.
- `issubclass(A, B)` — kiểm tra A có phải class con của B không.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `Dog('Rex').speak()` | Rex sủa: Gâu gâu! | str |
| `Cat('Mun').speak()` | Mun kêu: Meo meo! | str |
| `Puppy('Bun').speak() — super()` | Bun sủa: Gâu gâu! (giọng nhỏ xíu) | str |
| `isinstance(Dog('x'), Animal)` | True | bool |
| `issubclass(Puppy, Animal)` | True | bool |

### Hiểu thế nào
- `Puppy` kết quả ghép từ 2 phần: `super().speak()` (lấy của `Dog`) + `" (giọng nhỏ xíu)"`.
  → Đây là cách **tái sử dụng** code cha mà vẫn bổ sung thêm.
- `isinstance` và `issubclass` ra `True` vì `Dog`/`Puppy` đều là "con cháu" của `Animal`.

---

## B3 — Xử lý lỗi (Error Handling)
📍 URL: `/lesson/basic/errors` · Hàm: `oop_errors()` ([lessons_basic.py:142](lessons_basic.py#L142))

### Học gì
- **try / except**: thử chạy code, nếu lỗi thì **bắt** lại thay vì để app crash.
  ```python
  try:
      return a / b
  except ZeroDivisionError:
      return "Lỗi: không thể chia cho 0"
  ```
- **raise**: chủ động "ném" ra lỗi khi dữ liệu không hợp lệ.
- **Exception tự định nghĩa**: `class InvalidOrderError(Exception)` — tạo loại lỗi riêng cho nghiệp vụ.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `divide(10, 2)` | 5.0 | float |
| `divide(10, 0) — bắt lỗi` | Lỗi: không thể chia cho 0 | str |
| `process_order(hợp lệ)` | Đã xử lý: laptop x2 | str |
| `process_order(thiếu product)` | Lỗi đơn hàng: Đơn hàng thiếu tên sản phẩm | str |
| `process_order(quantity=0)` | Lỗi đơn hàng: Số lượng phải lớn hơn 0 | str |

### Hiểu thế nào
- `10 / 0` bình thường sẽ làm chương trình **dừng đột ngột**. Nhờ `try/except`, app vẫn chạy tiếp và trả thông báo thân thiện.
- `raise InvalidOrderError(...)` cho phép bạn **tự đặt luật**: đơn hàng phải có sản phẩm và số lượng > 0.
- Đây là kỹ năng cực kỳ quan trọng để app **không bị sập** khi gặp dữ liệu xấu.

---

## B4 — Import Module
📍 URL: `/lesson/basic/imports` · Hàm: `oop_imports()` ([lessons_basic.py:179](lessons_basic.py#L179))

### Học gì
- **Module/thư viện**: code có sẵn người khác viết, mình dùng lại bằng `import`.
  - `import math` → dùng `math.sqrt()`, `math.pi`.
  - `from collections import Counter` → `Counter` đếm số lần xuất hiện.
- Tự viết hàm tiện ích `clean()` để chuẩn hóa chuỗi (xóa khoảng trắng thừa).

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `math.sqrt(144)` | 12.0 | float |
| `round(math.pi, 4)` | 3.1416 | float |
| `Counter(words).most_common(2)` | [('python', 3), ('ai', 2)] | list |
| `clean(' AI   Training... ')` | AI Training Bootcamp 2026 | str |

### Hiểu thế nào
- Không cần tự viết hàm căn bậc hai — `math` đã có sẵn. **Lập trình = biết tận dụng thư viện.**
- `Counter(...).most_common(2)` đếm và trả về 2 từ xuất hiện nhiều nhất → rất hữu ích khi phân tích dữ liệu.
- `" ".join(text.split())` là mẹo kinh điển để gộp nhiều khoảng trắng thành một.

---

# PHẦN C — Dữ liệu: JSON & Regex (Day 4–5)

---

## C1 — JSON
📍 URL: `/lesson/basic/json` · Hàm: `data_json()` ([lessons_basic.py:197](lessons_basic.py#L197))

### Học gì
- **JSON** là định dạng trao đổi dữ liệu phổ biến nhất (API, file cấu hình...). Trông giống dict Python.
- `json.dumps(obj)` — biến dict Python **thành chuỗi JSON** (để gửi đi/lưu file).
- `json.loads(chuỗi)` — biến chuỗi JSON **thành dict Python** (để xử lý).
- Truy cập dữ liệu lồng nhau: `config["ocr"]["engine"]`.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả | Kiểu |
|-----------|---------|------|
| `json.dumps(config)` | {"app_name": "OCR Pipeline", ...} | str |
| `Truy cập config['ocr']['engine']` | tesseract | str |
| `json.loads(chuỗi)['name']` | Duc | str |
| `json.loads(...)['passed']` | True | bool |
| `Điểm trung bình từng SV` | {'An': 7.5, 'Binh': 8.5} | dict |

### Hiểu thế nào
- Nhớ cặp đối nghịch: **dumps = dump string (xuất)**, **loads = load string (nhập)**.
- Trong JSON `true` (chữ thường) → khi `loads` thành Python thì là `True` (chữ hoa).
- API tỷ giá ở Bài C/Phần D trả về **chính là JSON** — đây là lý do bài này quan trọng.

---

## C2 — Regex (Biểu thức chính quy)
📍 URL: `/lesson/basic/regex` · Hàm: `data_regex()` ([lessons_basic.py:225](lessons_basic.py#L225))

### Học gì
- **Regex** = mẫu (pattern) để **tìm/trích** chuỗi theo quy luật (email, số điện thoại, ngày tháng...).
- `re.findall(pattern, text)` — tìm **tất cả** đoạn khớp mẫu.
- Một vài ký hiệu:
  - `\d` = một chữ số, `\w` = chữ/số/gạch dưới.
  - `+` = một hoặc nhiều lần, `{4}` = đúng 4 lần.
  - `[ ]` = một trong các ký tự bên trong.

### Chạy hiển thị thế nào

| Biểu thức | Kết quả |
|-----------|---------|
| `Trích email` | ['hongduc10111999@gmail.com', 'support@company.vn'] |
| `Trích số điện thoại` | ['0912-345-678'] |
| `Trích ngày (ISO)` | ['2026-06-01'] |
| `Trích giá tiền` | ['1,200.00'] |
| `Trích URL` | ['https://aistudio.google.com'] |

### Hiểu thế nào
- `\d{4}-\d{2}-\d{2}` đọc là "4 số − 2 số − 2 số" → đúng định dạng ngày `2026-06-01`.
- Regex trông khó nhưng cực mạnh: chỉ 1 dòng đã tách được mọi email trong một đoạn văn dài.
- Mẹo học: đọc pattern từ trái sang phải như đọc "công thức mô tả chuỗi cần tìm".

---

# PHẦN D — 3 Bài thực hành xử lý dữ liệu thật

Khác với Phần A–C (chạy code rồi đổ ra bảng tĩnh), 3 bài này có **tương tác động**:
frontend gọi **API** của backend bằng JavaScript (`fetch`), backend trả **JSON**, frontend vẽ ra bảng.

Dữ liệu lấy từ file [../day4_5_data/data/orders.csv](../day4_5_data/data/orders.csv) (12 đơn hàng mẫu).
Hàm đọc dữ liệu chung: `load_orders()` ([app.py:16](app.py#L16)) — dùng **pandas** đọc CSV, đổi định dạng ngày,
và tính thêm cột `total_usd = quantity × unit_price_usd`.

---

## D1 — Đơn hàng (lọc theo danh mục)
📍 Trang: `/lesson/orders` · API: `/api/orders` ([app.py:59](app.py#L59))

### Học gì
- Đọc file CSV bằng **pandas**: `pd.read_csv(...)`.
- **Lọc dữ liệu** theo điều kiện: `df[df["category"] == category]`.
- Trả dữ liệu về frontend dạng **JSON**: `df.to_dict(orient="records")`.
- Frontend dùng **JavaScript `fetch`** để gọi API và vẽ bảng (xem [templates/orders.html](templates/orders.html#L47)).

### Thao tác
1. Mở trang `/lesson/orders`.
2. Ở ô **Danh mục**, chọn ví dụ `Electronics`, `Audio`, `Accessories` hoặc `All`.
3. Bảng tự cập nhật ngay (không cần tải lại trang).

### Chạy hiển thị thế nào
- Một **bảng đơn hàng**: Mã đơn · Ngày · Khách · Sản phẩm · Danh mục · SL · Tổng (USD).
- Phía trên hiện số đơn, ví dụ chọn `Electronics` → "4 đơn".
- Mỗi lần đổi danh mục, JS gọi `GET /api/orders?category=Electronics`, Python lọc và trả về.

### Hiểu thế nào
- **Luồng đầy đủ:** chọn danh mục → JS `fetch('/api/orders?category=...')` → Flask đọc CSV, lọc bằng pandas → trả JSON → JS dựng lại các dòng `<tr>` trong bảng.
- `df[df["category"] == category]` là **lọc theo điều kiện**: chỉ giữ dòng có danh mục khớp.
- Bạn có thể tự kiểm chứng bằng cách gõ thẳng URL `http://127.0.0.1:5001/api/orders?category=Audio` để xem **JSON thô**.

---

## D2 — Thống kê doanh thu
📍 Trang: `/lesson/stats` · API: `/api/stats` ([app.py:74](app.py#L74))

### Học gì
- **Gộp nhóm & tính tổng** bằng pandas: `df.groupby("category")["total_usd"].sum()`.
- Sắp xếp kết quả: `.sort_values(ascending=False)` (giảm dần).
- Làm tròn & chuyển sang dict để trả JSON: `.round(2).to_dict()`.

### Thao tác
Chỉ cần mở trang `/lesson/stats`. Backend tự tính khi trang gọi API.

### Chạy hiển thị thế nào
- **Tổng số đơn** và **tổng doanh thu (USD)**.
- **Doanh thu theo danh mục** (Electronics / Audio / Accessories), từ cao xuống thấp.
- **Doanh thu theo khách hàng**, từ cao xuống thấp.

### Hiểu thế nào
- `groupby("category")` = "gom các đơn cùng danh mục lại thành nhóm", rồi `.sum()` cộng doanh thu mỗi nhóm.
  → Đây là phép phân tích dữ liệu **cốt lõi** (giống Pivot Table trong Excel).
- Ví dụ Electronics gồm các đơn laptop/màn hình giá cao → thường đứng đầu doanh thu.
- Xem JSON thô tại `http://127.0.0.1:5001/api/stats` để hiểu cấu trúc backend trả về.

---

## D3 — Tỷ giá (gọi API ngoài)
📍 Trang: `/lesson/exchange` · API: `/api/exchange` ([app.py:93](app.py#L93))

### Học gì
- **Gọi API bên ngoài** qua internet bằng thư viện `requests`: `requests.get(API_URL).json()`.
- Lấy tỷ giá từ JSON trả về: `data["rates"].get(currency)`.
- **Quy đổi tiền tệ**: `total_usd × rate`.

### Thao tác
1. Mở trang `/lesson/exchange`.
2. Bấm nút để Python gọi API tỷ giá và quy đổi tổng doanh thu sang VND (hoặc tiền tệ khác).

> ⚠️ Bài này **cần có internet** vì gọi tới `https://open.er-api.com`.
> Nếu mất mạng, bài sẽ báo lỗi — đây cũng là dịp hiểu vì sao cần `try/except` (Bài B3).

### Chạy hiển thị thế nào
- Hiển thị: loại tiền, **tỷ giá** hiện tại (ví dụ 1 USD ≈ 25.xxx VND), tổng USD và **số tiền sau quy đổi**.
- Tỷ giá là **thật, cập nhật theo thời gian thực** từ API → mỗi ngày có thể khác nhau.

### Hiểu thế nào
- Đây là bài tổng hợp: **đọc CSV (pandas) + gọi API (requests) + xử lý JSON** — đúng quy trình thực tế của một backend.
- `requests.get(url).json()` = "tải dữ liệu từ URL về rồi đọc thành dict Python".
- Tự kiểm chứng: mở `http://127.0.0.1:5001/api/exchange?currency=VND` để xem JSON tỷ giá thô.

---

# 🎯 Lộ trình học gợi ý

1. **Đọc mục 0**, chạy app thành công, dạo qua trang chủ.
2. Học **Phần A** (A1→A4) theo thứ tự — đây là nền tảng, đừng bỏ qua.
3. Học **Phần B** (OOP) — cần hiểu A trước.
4. Học **Phần C** (JSON/Regex) — chuẩn bị cho dữ liệu thật.
5. Làm **Phần D** (3 bài thực hành) — ráp tất cả lại thành app hoàn chỉnh.

### Cách học hiệu quả nhất
- Với mỗi bài: **mở URL xem kết quả** → **mở file `lessons_basic.py` đọc code tương ứng** → **thử sửa một giá trị, lưu, F5 trang** để xem kết quả đổi thế nào.
- Ví dụ: đổi `age = 27` thành `age = 30` trong [lessons_basic.py:3](lessons_basic.py#L3), lưu, tải lại trang `/lesson/basic/variables` → thấy số tuổi đổi. Đó là lúc bạn thực sự **hiểu**.

> 📌 Toàn bộ kết quả trong tài liệu này được lấy trực tiếp từ code của bạn, nên bạn có thể đối chiếu 1:1 khi chạy thật.
