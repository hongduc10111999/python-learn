import re # Import module re để dùng biểu thức chính quy (regular expression) - tìm kiếm theo mẫu

text = """
Liên hệ: hongduc10111999@gmail.com hoặc support@company.vn
Hotline: 0912-345-678, văn phòng: 028 3822 9999
Đơn hàng #1001 ngày 2026-06-01 trị giá $1,200.00
Đơn hàng #1002 ngày 2026-06-03 trị giá $75.50
Website: https://aistudio.google.com và https://console.groq.com
""" # Chuỗi văn bản nhiều dòng (dùng 3 dấu nháy) để thực hành tìm kiếm mẫu

emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text) # Tìm tất cả email: phần tên + @ + tên miền + . + đuôi
print("Emails:", emails) # In danh sách email tìm được

phones = re.findall(r"0\d{2,3}[- ]?\d{3,4}[- ]?\d{3,4}", text) # Tìm số điện thoại: bắt đầu bằng 0, có thể có dấu gạch hoặc khoảng trắng
print("Phones:", phones) # In danh sách số điện thoại

dates = re.findall(r"\d{4}-\d{2}-\d{2}", text) # Tìm ngày dạng YYYY-MM-DD (4 số - 2 số - 2 số)
print("Dates:", dates) # In danh sách ngày

prices = re.findall(r"\$([\d,]+\.\d{2})", text) # Tìm giá tiền có dấu $; phần trong ngoặc () là phần được lấy ra (số tiền không gồm $)
print("Prices:", prices) # In danh sách giá tiền

urls = re.findall(r"https?://[^\s]+", text) # Tìm URL: http hoặc https, theo sau là các ký tự không phải khoảng trắng
print("URLs:", urls) # In danh sách URL

order_pattern = re.compile(r"#(?P<id>\d+) ngày (?P<date>\d{4}-\d{2}-\d{2})") # Biên dịch sẵn mẫu, đặt tên nhóm: id và date (?P<tên>)
for match in order_pattern.finditer(text): # Duyệt qua từng kết quả khớp với mẫu trong văn bản
    print(f"Đơn {match.group('id')} đặt ngày {match.group('date')}") # Lấy ra giá trị theo tên nhóm và in

masked = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL ĐÃ ẨN]", text) # Thay tất cả email bằng chữ "[EMAIL ĐÃ ẨN]" (re.sub = thay thế)
print(masked) # In văn bản đã che email

messy = "Hà   Nội,Việt    Nam" # Chuỗi có nhiều khoảng trắng thừa
cleaned = re.sub(r"\s+", " ", messy) # Thay mọi cụm khoảng trắng (\s+) bằng đúng 1 dấu cách
print(cleaned) # In chuỗi đã làm sạch

if re.match(r"^\d{4}-\d{2}-\d{2}$", "2026-06-11"): # re.match kiểm tra chuỗi có khớp mẫu từ đầu không; ^ và $ neo đầu và cuối chuỗi
    print("Chuỗi đúng định dạng ngày ISO") # In nếu chuỗi đúng định dạng ngày
