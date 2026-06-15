import requests # Import thư viện requests để gọi API (gửi yêu cầu HTTP qua mạng)

response = requests.get("https://api.github.com/users/torvalds", timeout=10) # Gửi yêu cầu GET lấy thông tin user torvalds; timeout=10 giây
print("Status:", response.status_code) # In mã trạng thái HTTP (200 = thành công)

user = response.json() # Chuyển nội dung trả về (dạng JSON) thành dictionary Python
print("Tên:", user["name"]) # In tên người dùng
print("Số repo public:", user["public_repos"]) # In số kho mã nguồn công khai
print("Followers:", user["followers"]) # In số người theo dõi

params = {"q": "language:python", "sort": "stars", "per_page": 3} # Tham số tìm kiếm: ngôn ngữ python, sắp theo sao, lấy 3 kết quả
response = requests.get( # Gửi yêu cầu tìm kiếm repository
    "https://api.github.com/search/repositories", params=params, timeout=10 # params sẽ được thêm vào URL thành chuỗi truy vấn
)
response.raise_for_status() # Nếu yêu cầu lỗi (mã 4xx/5xx) thì ném ra lỗi ngay

for repo in response.json()["items"]: # Duyệt qua danh sách repository trong kết quả trả về
    print(f"{repo['full_name']} - {repo['stargazers_count']:,} sao") # In tên repo và số sao (có dấu phẩy ngăn cách hàng nghìn)

try: # Thử gọi tới một địa chỉ không tồn tại để minh họa xử lý lỗi
    bad = requests.get("https://api.github.com/khong-ton-tai", timeout=10) # Gọi đến endpoint không tồn tại
    bad.raise_for_status() # Sẽ ném lỗi vì server trả về mã 404
except requests.HTTPError as e: # Bắt lỗi HTTP (server trả về mã lỗi)
    print("Lỗi HTTP:", e.response.status_code) # In ra mã lỗi cụ thể
except requests.ConnectionError: # Bắt lỗi khi không kết nối được mạng
    print("Không kết nối được mạng") # Thông báo lỗi mạng
except requests.Timeout: # Bắt lỗi khi server phản hồi quá lâu (vượt timeout)
    print("Hết thời gian chờ") # Thông báo hết thời gian chờ
