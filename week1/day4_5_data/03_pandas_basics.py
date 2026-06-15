from pathlib import Path # Import Path để làm việc với đường dẫn file

import pandas as pd # Import thư viện pandas (chuyên xử lý dữ liệu dạng bảng), đặt tên ngắn là pd

DATA_DIR = Path(__file__).parent / "data" # Trỏ tới thư mục "data" cùng cấp với file này

df = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["date"]) # Đọc file CSV vào DataFrame; parse_dates chuyển cột "date" thành kiểu ngày tháng

print(df.head()) # In 5 dòng đầu tiên của bảng
print(df.info()) # In thông tin tổng quan: tên cột, kiểu dữ liệu, số dòng không rỗng
print(df.describe()) # In thống kê mô tả (trung bình, min, max...) cho các cột số

df["total_usd"] = df["quantity"] * df["unit_price_usd"] # Tạo cột mới "total_usd" = số lượng x đơn giá (pandas tính trên toàn bộ cột cùng lúc)
print(df[["order_id", "product", "total_usd"]]) # In bảng chỉ gồm 3 cột được chọn

expensive = df[df["total_usd"] > 500] # Lọc ra các dòng có total_usd lớn hơn 500
print(expensive[["product", "total_usd"]]) # In sản phẩm và thành tiền của các đơn đắt tiền

by_category = df.groupby("category").agg( # Nhóm các dòng theo "category", rồi tính toán tổng hợp (aggregate)
    total_revenue=("total_usd", "sum"), # Tạo cột total_revenue = tổng total_usd của mỗi nhóm
    order_count=("order_id", "count"), # Tạo cột order_count = đếm số đơn trong mỗi nhóm
    avg_order=("total_usd", "mean"), # Tạo cột avg_order = giá trị đơn trung bình của mỗi nhóm
)
print(by_category.sort_values("total_revenue", ascending=False)) # Sắp xếp theo doanh thu giảm dần và in ra

by_customer = df.groupby("customer")["total_usd"].sum().sort_values(ascending=False) # Nhóm theo khách hàng, tính tổng chi tiêu, sắp xếp giảm dần
print(by_customer) # In doanh thu theo từng khách hàng

daily = df.groupby("date")["total_usd"].sum() # Nhóm theo ngày, tính tổng doanh thu mỗi ngày
print(daily) # In doanh thu theo từng ngày

top3 = df.nlargest(3, "total_usd")[["product", "customer", "total_usd"]] # Lấy 3 đơn có total_usd lớn nhất, chỉ giữ 3 cột
print(top3) # In ra 3 đơn hàng giá trị cao nhất

out_path = DATA_DIR / "category_report.csv" # Đường dẫn file báo cáo sẽ ghi ra
by_category.to_csv(out_path) # Ghi bảng tổng hợp theo danh mục ra file CSV
print("Đã ghi:", out_path) # Thông báo đã ghi xong
