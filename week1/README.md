# Tuần 1: Nền tảng Python

Mục tiêu chung của tuần: nắm vững cú pháp Python, lập trình hướng đối tượng,
xử lý dữ liệu (CSV/JSON/Pandas/Regex) và gọi API — đủ để tự xây một pipeline
dữ liệu nhỏ hoàn chỉnh.


## Cách chạy

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Chạy từng file bài học, ví dụ:

    python day1_2_syntax/01_variables_types.py


## Lộ trình & đánh giá theo từng bài

Mỗi bài gồm 3 phần: Mục tiêu (học được gì), Phương thức (làm thế nào),
Đánh giá kết quả (tự kiểm tra đã đạt chưa).


### Day 1–2 — Cú pháp cơ bản (day1_2_syntax/)

01_variables_types.py
- Mục tiêu: biến, kiểu dữ liệu (str/int/float/bool), f-string, ép kiểu, thao tác chuỗi.
- Phương thức: khai báo biến và in type(), format chuỗi, gọi .upper()/.split()/.replace().
- Đánh giá: giải thích được khác biệt giữa các kiểu; ép "100" thành số và tính toán đúng.

02_lists_dicts.py
- Mục tiêu: list (append/insert/slice/sort), dict (get/key), list comprehension.
- Phương thức: thao tác list, lọc số chẵn bằng comprehension, truy cập dict có giá trị mặc định.
- Đánh giá: viết được comprehension lọc/biến đổi; dùng .get() để tránh KeyError.

03_functions.py
- Mục tiêu: hàm, tham số mặc định, trả nhiều giá trị, *args/**kwargs.
- Phương thức: định nghĩa hàm calc_total, stats; unpack tuple kết quả.
- Đánh giá: viết hàm có tham số mặc định; nhận và unpack nhiều giá trị trả về.

04_loops_lambda.py
- Mục tiêu: for/while, range, break/continue, enumerate, lambda/map/sorted.
- Phương thức: lặp với bước nhảy, đếm ngược, đánh số sản phẩm, sắp xếp bằng lambda.
- Đánh giá: dùng đúng break vs continue; sắp xếp list theo key tùy chỉnh.


### Day 3 — Lập trình hướng đối tượng (day3_oop/)

01_classes.py
- Mục tiêu: class, __init__, method, __str__.
- Phương thức: xây class BankAccount với deposit/withdraw có kiểm tra hợp lệ.
- Đánh giá: tạo object, gọi method; hiểu vai trò của self và __str__.

02_inheritance.py
- Mục tiêu: kế thừa, override, super(), đa hình.
- Phương thức: Animal → Dog/Cat → Puppy, override method speak().
- Đánh giá: override method và gọi lại lớp cha bằng super().

03_error_handling.py
- Mục tiêu: try/except/else/finally, exception tự định nghĩa.
- Phương thức: hàm divide bắt nhiều loại lỗi; InvalidOrderError cho process_order.
- Đánh giá: bắt đúng loại exception; biết khi nào nên tự định nghĩa exception.

04_imports.py (+ utils/text_tools.py)
- Mục tiêu: import thư viện chuẩn và module tự viết.
- Phương thức: dùng math/datetime/Counter; import hàm từ utils.text_tools.
- Đánh giá: tách code dùng lại thành module và import được.


### Day 4–5 — Xử lý dữ liệu (day4_5_data/)

Dữ liệu mẫu nằm trong day4_5_data/data/ (orders.csv, config.json, ...).

01_csv_basics.py
- Mục tiêu: đọc/ghi CSV bằng thư viện chuẩn csv.
- Phương thức: DictReader đọc orders.csv, tính doanh thu, ghi file tổng hợp.
- Đánh giá: đọc CSV thành list dict, tính toán và ghi ra CSV mới.

02_json_basics.py
- Mục tiêu: đọc/ghi JSON, parse chuỗi JSON.
- Phương thức: json.dump/json.load với ensure_ascii=False, json.loads.
- Đánh giá: ghi JSON có dấu tiếng Việt đúng; truy cập JSON lồng nhau.

03_pandas_basics.py
- Mục tiêu: Pandas — đọc CSV, describe, lọc, groupby/agg.
- Phương thức: tạo cột mới, lọc đơn > $500, gộp nhóm theo category.
- Đánh giá: dùng groupby().agg() ra báo cáo; lọc DataFrame theo điều kiện.

04_regex.py
- Mục tiêu: biểu thức chính quy với re.
- Phương thức: re.findall trích email, số điện thoại, ngày, giá tiền, URL.
- Đánh giá: viết pattern trích đúng dữ liệu từ văn bản hỗn hợp.


### Day 6–7 — Gọi API & dự án nhỏ (day6_7_api/)

01_requests_demo.py
- Mục tiêu: gọi REST API bằng requests, xử lý lỗi HTTP.
- Phương thức: GET GitHub API, truyền params, raise_for_status, bắt HTTPError/ConnectionError.
- Đánh giá: gọi API, đọc JSON trả về và xử lý lỗi mạng/HTTP.

mini_project/  (Deliverable cuối tuần)
- Mục tiêu: pipeline dữ liệu hoàn chỉnh.
- Phương thức: đọc orders.csv → xử lý pandas → gọi API tỷ giá (đọc config từ .env)
  → xuất report.csv + summary.json.
- Đánh giá: pipeline chạy end-to-end, tạo đúng file output, đọc config từ .env.


## Deliverable cuối tuần

    cd day6_7_api/mini_project
    cp .env.example .env        # chỉnh sửa nếu cần
    python main.py

Luồng xử lý: đọc data/orders.csv → xử lý bằng pandas → gọi API tỷ giá USD
→ quy đổi và xuất output/report.csv + output/summary.json.

Tiêu chí hoàn thành: chạy không lỗi, tạo đủ file output, số liệu quy đổi khớp
với tỷ giá API, và cấu hình (API URL, tiền tệ đích) đọc được từ .env.


## Demo web (mở rộng, ngoài chương trình bắt buộc)

Cùng dữ liệu orders.csv, dựng UI tương tác để củng cố kiến thức:

    streamlit run day6_7_api/web_demo/app.py    # Streamlit
    python web_app/app.py                       # Flask
