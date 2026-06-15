import csv # Import module csv để đọc/ghi file CSV
from pathlib import Path # Import Path để làm việc với đường dẫn file một cách tiện lợi

DATA_DIR = Path(__file__).parent / "data" # Lấy thư mục chứa file này, rồi trỏ tới thư mục con "data"

with open(DATA_DIR / "orders.csv", newline="", encoding="utf-8") as f: # Mở file orders.csv để đọc (encoding utf-8 để đọc tiếng Việt)
    reader = csv.DictReader(f) # Tạo bộ đọc CSV trả về mỗi dòng dưới dạng dictionary (khóa là tên cột)
    orders = list(reader) # Chuyển tất cả các dòng thành một danh sách

print("Tổng số đơn:", len(orders)) # In ra tổng số đơn hàng
print("Đơn đầu tiên:", orders[0]) # In ra đơn hàng đầu tiên

total_revenue = 0 # Biến tích lũy tổng doanh thu, bắt đầu từ 0
for order in orders: # Duyệt qua từng đơn hàng
    total_revenue += int(order["quantity"]) * float(order["unit_price_usd"]) # Cộng dồn (số lượng x đơn giá); int và float chuyển chuỗi thành số
print(f"Tổng doanh thu: ${total_revenue:,.2f}") # In tổng doanh thu, định dạng có dấu phẩy và 2 chữ số thập phân

electronics = [o for o in orders if o["category"] == "Electronics"] # Lọc ra các đơn thuộc danh mục Electronics (list comprehension)
print("Số đơn Electronics:", len(electronics)) # In số lượng đơn Electronics

summary_rows = [] # Danh sách rỗng để chứa các dòng tóm tắt
for order in orders: # Duyệt qua từng đơn hàng
    summary_rows.append( # Thêm một dòng tóm tắt mới vào danh sách
        { # Mỗi dòng là một dictionary
            "order_id": order["order_id"], # Mã đơn hàng
            "product": order["product"], # Tên sản phẩm
            "total_usd": int(order["quantity"]) * float(order["unit_price_usd"]), # Thành tiền của đơn
        }
    )

out_path = DATA_DIR / "order_totals.csv" # Đường dẫn file CSV sẽ ghi kết quả
with open(out_path, "w", newline="", encoding="utf-8") as f: # Mở file ở chế độ ghi ("w")
    writer = csv.DictWriter(f, fieldnames=["order_id", "product", "total_usd"]) # Tạo bộ ghi CSV, khai báo tên các cột
    writer.writeheader() # Ghi dòng tiêu đề (tên cột) vào file
    writer.writerows(summary_rows) # Ghi tất cả các dòng dữ liệu vào file

print("Đã ghi file:", out_path) # Thông báo đã ghi file xong
