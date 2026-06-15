import json # Module đọc/ghi JSON
import shutil # Module thao tác file/thư mục cấp cao (vd: xóa cả thư mục)
from pathlib import Path # Làm việc với đường dẫn file

import pandas as pd # Thư viện xử lý dữ liệu dạng bảng
import requests # Thư viện gọi API qua mạng
from dotenv import load_dotenv # Hàm đọc biến môi trường từ file .env
import os # Module truy cập biến môi trường của hệ điều hành

BASE_DIR = Path(__file__).parent # Thư mục chứa file main.py này
DATA_FILE = BASE_DIR.parent.parent / "day4_5_data" / "data" / "orders.csv" # Đường dẫn tới file orders.csv (đi lên 2 cấp rồi vào day4_5_data)
OUTPUT_DIR = BASE_DIR / "output" # Thư mục để xuất kết quả báo cáo

load_dotenv(BASE_DIR / ".env") # Nạp các biến cấu hình từ file .env vào môi trường
API_URL = os.getenv("EXCHANGE_API_URL", "https://open.er-api.com/v6/latest/USD") # Lấy URL API tỷ giá từ .env, nếu không có thì dùng giá trị mặc định
TARGET_CURRENCY = os.getenv("TARGET_CURRENCY", "VND") # Lấy loại tiền cần quy đổi, mặc định là VND


def load_orders(path): # Hàm đọc dữ liệu đơn hàng từ file CSV
    df = pd.read_csv(path, parse_dates=["date"]) # Đọc CSV vào DataFrame, chuyển cột date thành kiểu ngày
    df["total_usd"] = df["quantity"] * df["unit_price_usd"] # Tạo cột thành tiền = số lượng x đơn giá
    return df # Trả về DataFrame đã xử lý


def fetch_exchange_rate(currency): # Hàm gọi API lấy tỷ giá hối đoái
    response = requests.get(API_URL, timeout=10) # Gửi yêu cầu GET tới API tỷ giá
    response.raise_for_status() # Ném lỗi nếu yêu cầu thất bại
    data = response.json() # Chuyển kết quả JSON thành dictionary
    if data.get("result") != "success": # Kiểm tra API có báo thành công không
        raise RuntimeError(f"API trả về lỗi: {data}") # Nếu không thành công thì ném lỗi
    rate = data["rates"].get(currency) # Lấy tỷ giá của loại tiền cần tìm
    if rate is None: # Nếu không tìm thấy tỷ giá cho loại tiền đó
        raise ValueError(f"Không tìm thấy tỷ giá cho {currency}") # Ném lỗi báo không có tỷ giá
    return rate # Trả về tỷ giá


def build_report(df, rate, currency): # Hàm tạo báo cáo từ dữ liệu và tỷ giá
    df = df.copy() # Tạo bản sao để không thay đổi dữ liệu gốc
    df[f"total_{currency.lower()}"] = (df["total_usd"] * rate).round(0) # Thêm cột thành tiền theo tiền tệ đích, làm tròn về số nguyên

    by_category = df.groupby("category").agg( # Nhóm theo danh mục và tính tổng hợp
        order_count=("order_id", "count"), # Đếm số đơn trong mỗi danh mục
        revenue_usd=("total_usd", "sum"), # Tổng doanh thu USD theo danh mục
    )
    by_category[f"revenue_{currency.lower()}"] = ( # Thêm cột doanh thu theo tiền tệ đích
        by_category["revenue_usd"] * rate # Nhân doanh thu USD với tỷ giá
    ).round(0) # Làm tròn về số nguyên

    summary = { # Dictionary tóm tắt toàn bộ báo cáo
        "report_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), # Thời điểm tạo báo cáo (định dạng năm-tháng-ngày giờ)
        "exchange_rate": {"from": "USD", "to": currency, "rate": rate}, # Thông tin tỷ giá đã dùng
        "total_orders": int(len(df)), # Tổng số đơn hàng
        "total_revenue_usd": round(float(df["total_usd"].sum()), 2), # Tổng doanh thu USD, làm tròn 2 chữ số
        f"total_revenue_{currency.lower()}": round( # Tổng doanh thu theo tiền tệ đích
            float(df["total_usd"].sum() * rate) # Tổng USD nhân tỷ giá
        ),
        "top_customer": df.groupby("customer")["total_usd"].sum().idxmax(), # Khách hàng chi tiêu nhiều nhất (idxmax lấy tên có giá trị lớn nhất)
        "best_selling_category": by_category["revenue_usd"].idxmax(), # Danh mục có doanh thu cao nhất
    }
    return df, by_category, summary # Trả về 3 kết quả: bảng chi tiết, bảng theo danh mục, và tóm tắt


def export(df, by_category, summary): # Hàm xuất các báo cáo ra file
    if OUTPUT_DIR.exists(): # Nếu thư mục output đã tồn tại
        shutil.rmtree(OUTPUT_DIR) # Xóa toàn bộ thư mục cũ để làm sạch
    OUTPUT_DIR.mkdir() # Tạo lại thư mục output mới

    df.to_csv(OUTPUT_DIR / "report.csv", index=False) # Ghi bảng chi tiết ra CSV (không kèm cột chỉ số)
    by_category.to_csv(OUTPUT_DIR / "category_report.csv") # Ghi bảng theo danh mục ra CSV
    with open(OUTPUT_DIR / "summary.json", "w", encoding="utf-8") as f: # Mở file summary.json để ghi
        json.dump(summary, f, indent=2, ensure_ascii=False) # Ghi phần tóm tắt ra JSON, giữ tiếng Việt và định dạng đẹp


def main(): # Hàm chính điều phối toàn bộ quy trình
    print("1. Đọc dữ liệu từ", DATA_FILE.name) # Bước 1: thông báo đang đọc dữ liệu
    df = load_orders(DATA_FILE) # Đọc dữ liệu đơn hàng
    print(f"   -> {len(df)} đơn hàng") # In số đơn hàng đã đọc

    print(f"2. Gọi API lấy tỷ giá USD -> {TARGET_CURRENCY}") # Bước 2: thông báo đang gọi API
    rate = fetch_exchange_rate(TARGET_CURRENCY) # Lấy tỷ giá từ API
    print(f"   -> 1 USD = {rate:,.0f} {TARGET_CURRENCY}") # In tỷ giá vừa lấy được

    print("3. Xử lý dữ liệu và tạo báo cáo") # Bước 3: thông báo đang tạo báo cáo
    df, by_category, summary = build_report(df, rate, TARGET_CURRENCY) # Tạo báo cáo từ dữ liệu và tỷ giá

    print("4. Xuất báo cáo ra thư mục", OUTPUT_DIR.name) # Bước 4: thông báo đang xuất file
    export(df, by_category, summary) # Ghi các báo cáo ra file

    print("\n===== TÓM TẮT =====") # In tiêu đề phần tóm tắt
    for key, value in summary.items(): # Duyệt qua từng mục trong phần tóm tắt
        print(f"{key}: {value}") # In ra từng cặp khóa - giá trị


if __name__ == "__main__": # Chỉ chạy main() khi file này được chạy trực tiếp (không phải khi bị import)
    main() # Gọi hàm chính để bắt đầu chương trình
