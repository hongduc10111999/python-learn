class BankAccount: # Định nghĩa một lớp (class) tên BankAccount - khuôn mẫu để tạo ra các tài khoản ngân hàng
    def __init__(self, owner, balance=0): # Hàm khởi tạo, tự động chạy khi tạo object mới; balance mặc định là 0
        self.owner = owner # Gán tên chủ tài khoản vào thuộc tính owner của object
        self.balance = balance # Gán số dư vào thuộc tính balance của object

    def deposit(self, amount): # Phương thức (method) nạp tiền vào tài khoản
        if amount <= 0: # Nếu số tiền nạp nhỏ hơn hoặc bằng 0
            raise ValueError("Số tiền nạp phải lớn hơn 0") # Ném ra lỗi báo số tiền không hợp lệ
        self.balance += amount # Cộng số tiền nạp vào số dư hiện tại
        return self.balance # Trả về số dư mới sau khi nạp

    def withdraw(self, amount): # Phương thức rút tiền khỏi tài khoản
        if amount > self.balance: # Nếu số tiền muốn rút lớn hơn số dư
            raise ValueError("Số dư không đủ") # Ném ra lỗi báo không đủ tiền
        self.balance -= amount # Trừ số tiền rút khỏi số dư hiện tại
        return self.balance # Trả về số dư mới sau khi rút

    def __str__(self): # Phương thức đặc biệt, quyết định object hiển thị thế nào khi print
        return f"Tài khoản của {self.owner}: {self.balance:,.0f} VND" # Định dạng chuỗi với dấu phẩy ngăn cách hàng nghìn, không có số thập phân


account = BankAccount("Duc", 500_000) # Tạo một tài khoản mới của "Duc" với số dư ban đầu 500.000 (dấu _ chỉ để dễ đọc)
account.deposit(200_000) # Nạp thêm 200.000 vào tài khoản
account.withdraw(100_000) # Rút 100.000 khỏi tài khoản
print(account) # In tài khoản ra (gọi tới hàm __str__ ở trên)


class Counter: # Định nghĩa lớp Counter để đếm số object đã được tạo
    total_created = 0 # Thuộc tính của lớp (class attribute) - dùng chung cho tất cả object, đếm tổng số object

    def __init__(self): # Hàm khởi tạo, chạy mỗi khi tạo một Counter mới
        Counter.total_created += 1 # Tăng biến đếm chung lên 1 mỗi lần có object mới

    @classmethod # Decorator đánh dấu đây là phương thức của lớp (nhận cls thay vì self)
    def how_many(cls): # Phương thức trả về số lượng object đã tạo
        return cls.total_created # Trả về giá trị biến đếm chung

    @staticmethod # Decorator đánh dấu đây là phương thức tĩnh (không cần self hay cls)
    def describe(): # Phương thức tĩnh mô tả lớp này làm gì
        return "Counter đếm số instance đã tạo" # Trả về chuỗi mô tả


a = Counter() # Tạo object Counter thứ nhất -> total_created = 1
b = Counter() # Tạo object Counter thứ hai -> total_created = 2
c = Counter() # Tạo object Counter thứ ba -> total_created = 3
print(Counter.how_many()) # In ra số lượng object đã tạo (kết quả: 3)
print(Counter.describe()) # In ra mô tả của lớp Counter
