from pathlib import Path # Làm việc với đường dẫn file

import pandas as pd # Thư viện xử lý dữ liệu dạng bảng
import requests # Thư viện gọi API qua mạng
import streamlit as st # Thư viện tạo web app đơn giản bằng Python, đặt tên ngắn là st

DATA_FILE = ( # Đường dẫn tới file orders.csv
    Path(__file__).parent.parent.parent # Đi lên 3 cấp thư mục từ file này
    / "day4_5_data" # Vào thư mục day4_5_data
    / "data" # Vào thư mục data
    / "orders.csv" # Tới file orders.csv
)
API_URL = "https://open.er-api.com/v6/latest/USD" # Địa chỉ API lấy tỷ giá USD

st.set_page_config(page_title="Order Dashboard", page_icon="📊", layout="wide") # Cấu hình trang: tiêu đề, biểu tượng, bố cục rộng
st.title("📊 Order Dashboard") # Hiển thị tiêu đề lớn của trang
st.caption("Tuần 1 AI Bootcamp") # Hiển thị dòng chú thích nhỏ dưới tiêu đề


@st.cache_data # Decorator: lưu cache kết quả để không phải đọc file lại mỗi lần tương tác
def load_orders(): # Hàm đọc dữ liệu đơn hàng
    df = pd.read_csv(DATA_FILE, parse_dates=["date"]) # Đọc CSV, chuyển cột date thành kiểu ngày
    df["total_usd"] = df["quantity"] * df["unit_price_usd"] # Tạo cột thành tiền = số lượng x đơn giá
    return df # Trả về DataFrame


@st.cache_data(ttl=3600) # Lưu cache kết quả trong 3600 giây (1 giờ) để hạn chế gọi API liên tục
def get_rate(currency): # Hàm lấy tỷ giá cho một loại tiền
    data = requests.get(API_URL, timeout=10).json() # Gọi API và chuyển kết quả thành dictionary
    return data["rates"][currency] # Trả về tỷ giá của loại tiền cần tìm


df = load_orders() # Đọc dữ liệu đơn hàng vào DataFrame

st.sidebar.header("Bộ lọc") # Tạo tiêu đề cho thanh bên trái (sidebar)
categories = st.sidebar.multiselect( # Tạo ô chọn nhiều danh mục ở sidebar
    "Danh mục", # Nhãn của ô chọn
    options=sorted(df["category"].unique()), # Các lựa chọn: danh sách danh mục không trùng, đã sắp xếp
    default=sorted(df["category"].unique()), # Mặc định chọn tất cả các danh mục
)
min_total = st.sidebar.slider("Giá trị đơn tối thiểu (USD)", 0, 1500, 0, step=50) # Thanh trượt chọn giá trị tối thiểu: từ 0 đến 1500, mặc định 0, bước 50

filtered = df[df["category"].isin(categories) & (df["total_usd"] >= min_total)] # Lọc dữ liệu theo danh mục đã chọn VÀ giá trị tối thiểu

col1, col2, col3 = st.columns(3) # Chia giao diện thành 3 cột để hiển thị các chỉ số
col1.metric("Số đơn", len(filtered)) # Cột 1: hiển thị số lượng đơn sau khi lọc
col2.metric("Doanh thu (USD)", f"${filtered['total_usd'].sum():,.0f}") # Cột 2: hiển thị tổng doanh thu USD
if st.sidebar.checkbox("Quy đổi sang VND"): # Nếu người dùng tích vào ô "Quy đổi sang VND"
    rate = get_rate("VND") # Lấy tỷ giá USD sang VND
    col3.metric("Doanh thu (VND)", f"{filtered['total_usd'].sum() * rate:,.0f} ₫") # Cột 3: hiển thị doanh thu quy đổi sang VND
    st.sidebar.success(f"1 USD = {rate:,.0f} VND") # Hiển thị thông báo tỷ giá ở sidebar

st.subheader("Danh sách đơn hàng") # Tiêu đề phụ cho bảng đơn hàng
st.dataframe(filtered, use_container_width=True) # Hiển thị bảng dữ liệu đã lọc, kéo rộng theo khung

st.subheader("Doanh thu theo danh mục") # Tiêu đề phụ cho biểu đồ cột
by_cat = filtered.groupby("category")["total_usd"].sum() # Tính tổng doanh thu theo từng danh mục
st.bar_chart(by_cat) # Vẽ biểu đồ cột doanh thu theo danh mục

st.subheader("Doanh thu theo ngày") # Tiêu đề phụ cho biểu đồ đường
by_day = filtered.groupby("date")["total_usd"].sum() # Tính tổng doanh thu theo từng ngày
st.line_chart(by_day) # Vẽ biểu đồ đường doanh thu theo ngày
