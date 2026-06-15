def variables_types():
    name = "Duc"
    age = 27
    height = 1.76
    is_learning = True
    text = "AI Training Bootcamp"
    price = 19.99
    return [
        ("name", name, type(name).__name__),
        ("age", age, type(age).__name__),
        ("height", height, type(height).__name__),
        ("is_learning", is_learning, type(is_learning).__name__),
        ("f-string", f"Xin chào {name}, năm sau bạn {age + 1} tuổi", "str"),
        ("text.upper()", text.upper(), "str"),
        ("text.split()", str(text.split(" ")), "list"),
        ('int("100") + 50', int("100") + 50, "int"),
        ("price định dạng", f"{price:.1f}", "str"),
    ]


def lists_dicts():
    fruits = ["apple", "banana", "orange", "mango"]
    numbers = [5, 2, 9, 1, 7]
    student = {"name": "Duc", "age": 27, "skills": ["Python", "SQL"]}
    scores = {"math": 8, "english": 7, "physics": 9}
    return [
        ("fruits đã sort", str(sorted(fruits)), "list"),
        ("fruits[0], fruits[-1]", f"{fruits[0]}, {fruits[-1]}", "str"),
        ("sum / max / min", f"{sum(numbers)} / {max(numbers)} / {min(numbers)}", "int"),
        ("bình phương (comprehension)", str([n * n for n in numbers]), "list"),
        ("lọc số chẵn", str([n for n in numbers if n % 2 == 0]), "list"),
        ("student['name']", student["name"], "str"),
        ("dict.get mặc định", student.get("email", "chưa có email"), "str"),
        ("môn đạt >= 8", str({k: v for k, v in scores.items() if v >= 8}), "dict"),
    ]


def functions():
    def calc_total(price, quantity=1, discount=0.0):
        return price * quantity * (1 - discount)

    def stats(numbers):
        return min(numbers), max(numbers), sum(numbers) / len(numbers)

    lowest, highest, average = stats([4, 8, 15, 16, 23, 42])
    return [
        ("calc_total(100)", calc_total(100), "float"),
        ("calc_total(100, 3)", calc_total(100, 3), "float"),
        ("calc_total(100, 2, 0.1)", calc_total(100, quantity=2, discount=0.1), "float"),
        ("stats() -> min", lowest, "int"),
        ("stats() -> max", highest, "int"),
        ("stats() -> trung bình", round(average, 2), "float"),
    ]


def loops_lambda():
    products = ["laptop", "mouse", "keyboard"]
    prices = [1000, 20, 50]
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    people = [
        {"name": "An", "age": 30},
        {"name": "Binh", "age": 22},
        {"name": "Chi", "age": 27},
    ]
    people_sorted = sorted(people, key=lambda p: p["age"])
    return [
        ("range(1, 10, 2)", str(list(range(1, 10, 2))), "list"),
        ("enumerate sản phẩm", str(list(enumerate(products, start=1))), "list"),
        ("zip tên + giá", str(list(zip(products, prices))), "list"),
        ("sort giảm dần (lambda)", str(sorted(nums, key=lambda n: -n)), "list"),
        ("sort theo tuổi", str([p["name"] for p in people_sorted]), "list"),
        ("map nhân đôi", str(list(map(lambda n: n * 2, nums))), "list"),
        ("filter > 4", str(list(filter(lambda n: n > 4, nums))), "list"),
    ]


def oop_classes():
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount
            return self.balance

        def withdraw(self, amount):
            self.balance -= amount
            return self.balance

        def __str__(self):
            return f"Tài khoản của {self.owner}: {self.balance:,.0f} VND"

    account = BankAccount("Duc", 500_000)
    account.deposit(200_000)
    account.withdraw(100_000)

    class Counter:
        total_created = 0

        def __init__(self):
            Counter.total_created += 1

    Counter(), Counter(), Counter()

    return [
        ("Tạo BankAccount('Duc', 500000)", "balance = 500,000", "BankAccount"),
        ("deposit(200000) rồi withdraw(100000)", str(account), "str"),
        ("Tạo 3 Counter, Counter.how_many()", Counter.total_created, "int"),
    ]


def oop_inheritance():
    class Animal:
        def __init__(self, name):
            self.name = name

        def speak(self):
            return f"{self.name} phát ra âm thanh"

    class Dog(Animal):
        def speak(self):
            return f"{self.name} sủa: Gâu gâu!"

    class Cat(Animal):
        def speak(self):
            return f"{self.name} kêu: Meo meo!"

    class Puppy(Dog):
        def speak(self):
            return super().speak() + " (giọng nhỏ xíu)"

    return [
        ("Dog('Rex').speak()", Dog("Rex").speak(), "str"),
        ("Cat('Mun').speak()", Cat("Mun").speak(), "str"),
        ("Puppy('Bun').speak() — super()", Puppy("Bun").speak(), "str"),
        ("isinstance(Dog('x'), Animal)", str(isinstance(Dog("x"), Animal)), "bool"),
        ("issubclass(Puppy, Animal)", str(issubclass(Puppy, Animal)), "bool"),
    ]


def oop_errors():
    class InvalidOrderError(Exception):
        pass

    def divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return "Lỗi: không thể chia cho 0"

    def process_order(order):
        if "product" not in order:
            raise InvalidOrderError("Đơn hàng thiếu tên sản phẩm")
        if order.get("quantity", 0) <= 0:
            raise InvalidOrderError("Số lượng phải lớn hơn 0")
        return f"Đã xử lý: {order['product']} x{order['quantity']}"

    results = []
    for order in [
        {"product": "laptop", "quantity": 2},
        {"quantity": 1},
        {"product": "mouse", "quantity": 0},
    ]:
        try:
            results.append(process_order(order))
        except InvalidOrderError as e:
            results.append(f"Lỗi đơn hàng: {e}")

    return [
        ("divide(10, 2)", divide(10, 2), "float"),
        ("divide(10, 0) — bắt lỗi", divide(10, 0), "str"),
        ("process_order(hợp lệ)", results[0], "str"),
        ("process_order(thiếu product)", results[1], "str"),
        ("process_order(quantity=0)", results[2], "str"),
    ]


def oop_imports():
    import math
    from collections import Counter

    def clean(text):
        return " ".join(text.split()).strip()

    words = ["python", "ai", "python", "ocr", "ai", "python"]
    messy = "  AI   Training    Bootcamp   2026  "
    return [
        ("math.sqrt(144)", math.sqrt(144), "float"),
        ("round(math.pi, 4)", round(math.pi, 4), "float"),
        ("Counter(words).most_common(2)", str(Counter(words).most_common(2)), "list"),
        ("clean(' AI   Training... ')", clean(messy), "str"),
        ("đếm số từ sau khi clean", len(clean(messy).split()), "int"),
    ]


def data_json():
    import json

    config = {
        "app_name": "OCR Pipeline",
        "version": "1.0",
        "languages": ["vie", "eng"],
        "ocr": {"engine": "tesseract", "dpi": 300},
    }
    text = '{"name": "Duc", "score": 9.5, "passed": true}'
    parsed = json.loads(text)
    students = [
        {"name": "An", "scores": {"python": 8, "sql": 7}},
        {"name": "Binh", "scores": {"python": 9, "sql": 8}},
    ]
    averages = {
        s["name"]: round(sum(s["scores"].values()) / len(s["scores"]), 1)
        for s in students
    }
    return [
        ("json.dumps(config)", json.dumps(config, ensure_ascii=False), "str"),
        ("Truy cập config['ocr']['engine']", config["ocr"]["engine"], "str"),
        ("json.loads(chuỗi)['name']", parsed["name"], "str"),
        ("json.loads(...)['passed']", str(parsed["passed"]), "bool"),
        ("Điểm trung bình từng SV", str(averages), "dict"),
    ]


def data_regex():
    import re

    text = (
        "Liên hệ: hongduc10111999@gmail.com hoặc support@company.vn\n"
        "Hotline: 0912-345-678\n"
        "Đơn #1001 ngày 2026-06-01 trị giá $1,200.00\n"
        "Website: https://aistudio.google.com"
    )
    return [
        ("Trích email", str(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)), "list"),
        ("Trích số điện thoại", str(re.findall(r"0\d{2,3}[- ]?\d{3,4}[- ]?\d{3,4}", text)), "list"),
        ("Trích ngày (ISO)", str(re.findall(r"\d{4}-\d{2}-\d{2}", text)), "list"),
        ("Trích giá tiền", str(re.findall(r"\$([\d,]+\.\d{2})", text)), "list"),
        ("Trích URL", str(re.findall(r"https?://[^\s]+", text)), "list"),
    ]


LESSONS = {
    "variables": {
        "title": "01 — Biến & Kiểu dữ liệu",
        "file": "day1_2_syntax/01_variables_types.py",
        "run": variables_types,
    },
    "lists": {
        "title": "02 — List & Dict",
        "file": "day1_2_syntax/02_lists_dicts.py",
        "run": lists_dicts,
    },
    "functions": {
        "title": "03 — Hàm",
        "file": "day1_2_syntax/03_functions.py",
        "run": functions,
    },
    "loops": {
        "title": "04 — Vòng lặp & Lambda",
        "file": "day1_2_syntax/04_loops_lambda.py",
        "run": loops_lambda,
    },
    "classes": {
        "title": "Day 3 · 01 — Class",
        "file": "day3_oop/01_classes.py",
        "run": oop_classes,
    },
    "inheritance": {
        "title": "Day 3 · 02 — Kế thừa",
        "file": "day3_oop/02_inheritance.py",
        "run": oop_inheritance,
    },
    "errors": {
        "title": "Day 3 · 03 — Xử lý lỗi",
        "file": "day3_oop/03_error_handling.py",
        "run": oop_errors,
    },
    "imports": {
        "title": "Day 3 · 04 — Import module",
        "file": "day3_oop/04_imports.py",
        "run": oop_imports,
    },
    "json": {
        "title": "Day 4–5 · JSON",
        "file": "day4_5_data/02_json_basics.py",
        "run": data_json,
    },
    "regex": {
        "title": "Day 4–5 · Regex",
        "file": "day4_5_data/04_regex.py",
        "run": data_regex,
    },
}
