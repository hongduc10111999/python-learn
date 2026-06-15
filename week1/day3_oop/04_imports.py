import math # Import toàn bộ module math (chứa các hàm toán học)
from datetime import date, timedelta # Chỉ import lớp date và timedelta từ module datetime
from collections import Counter # Import lớp Counter từ module collections (dùng để đếm)

from utils.text_tools import clean, word_count, truncate # Import 3 hàm tự viết từ file utils/text_tools.py

print(math.sqrt(144)) # Tính căn bậc hai của 144 -> 12.0
print(math.pi) # In ra hằng số pi (~3.14159)

today = date.today() # Lấy ngày hôm nay
demo_day = today + timedelta(days=1) # Cộng thêm 1 ngày để được ngày mai (timedelta là khoảng thời gian)
print("Hôm nay:", today) # In ngày hôm nay
print("Demo:", demo_day) # In ngày mai

words = ["python", "ai", "python", "ocr", "ai", "python"] # Danh sách các từ có lặp lại
print(Counter(words).most_common(2)) # Đếm số lần xuất hiện và lấy 2 từ phổ biến nhất

messy = "  AI   Training    Bootcamp   2026  " # Chuỗi có nhiều khoảng trắng thừa
print(clean(messy)) # Dùng hàm clean để xóa khoảng trắng thừa
print(word_count(messy)) # Đếm số từ trong chuỗi
print(truncate("Đây là một câu rất dài cần cắt ngắn lại")) # Cắt ngắn chuỗi nếu quá dài
