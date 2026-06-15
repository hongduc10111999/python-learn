def divide(a, b): # Hàm chia a cho b với xử lý lỗi đầy đủ
    try: # Khối try: thử chạy đoạn code có thể gây lỗi
        result = a / b # Thực hiện phép chia (có thể lỗi nếu b=0 hoặc sai kiểu dữ liệu)
    except ZeroDivisionError: # Bắt lỗi khi chia cho 0
        print("Không thể chia cho 0") # Thông báo lỗi cho người dùng
        return None # Trả về None vì không có kết quả hợp lệ
    except TypeError as e: # Bắt lỗi khi sai kiểu dữ liệu (vd: chia số cho chuỗi); 'as e' lưu chi tiết lỗi
        print("Sai kiểu dữ liệu:", e) # In ra thông tin chi tiết về lỗi
        return None # Trả về None vì không có kết quả hợp lệ
    else: # Khối else: chỉ chạy khi try KHÔNG có lỗi nào xảy ra
        return result # Trả về kết quả phép chia
    finally: # Khối finally: LUÔN chạy dù có lỗi hay không
        print(f"Đã xử lý phép chia {a} / {b}") # In ra thông báo đã xử lý xong


print(divide(10, 2)) # Chia bình thường -> in 5.0
print(divide(10, 0)) # Chia cho 0 -> kích hoạt ZeroDivisionError
print(divide(10, "abc")) # Chia cho chuỗi -> kích hoạt TypeError


class InvalidOrderError(Exception): # Định nghĩa một loại lỗi tùy chỉnh (custom exception), kế thừa từ Exception
    pass # 'pass' nghĩa là không thêm gì, chỉ cần một loại lỗi riêng để dễ phân biệt


def process_order(order): # Hàm xử lý một đơn hàng
    if "product" not in order: # Nếu đơn hàng không có khóa "product"
        raise InvalidOrderError("Đơn hàng thiếu tên sản phẩm") # Ném ra lỗi tùy chỉnh
    if order.get("quantity", 0) <= 0: # Nếu số lượng nhỏ hơn hoặc bằng 0 (mặc định 0 nếu không có khóa)
        raise InvalidOrderError("Số lượng phải lớn hơn 0") # Ném ra lỗi tùy chỉnh
    return f"Đã xử lý đơn: {order['product']} x{order['quantity']}" # Trả về thông báo xử lý thành công


orders = [ # Danh sách các đơn hàng để kiểm thử
    {"product": "laptop", "quantity": 2}, # Đơn hợp lệ
    {"quantity": 1}, # Đơn thiếu tên sản phẩm -> sẽ gây lỗi
    {"product": "mouse", "quantity": 0}, # Đơn có số lượng = 0 -> sẽ gây lỗi
]

for order in orders: # Duyệt qua từng đơn hàng
    try: # Thử xử lý đơn hàng
        print(process_order(order)) # In kết quả nếu xử lý thành công
    except InvalidOrderError as e: # Bắt lỗi tùy chỉnh nếu đơn hàng không hợp lệ
        print("Lỗi đơn hàng:", e) # In ra thông báo lỗi cụ thể

try: # Thử mở một file
    with open("khong_ton_tai.txt") as f: # Mở file không tồn tại (with tự động đóng file sau khi dùng)
        f.read() # Đọc nội dung file
except FileNotFoundError: # Bắt lỗi khi file không tồn tại
    print("File không tồn tại, bỏ qua") # Thông báo và bỏ qua thay vì làm dừng chương trình
