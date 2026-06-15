import json # Import module json để đọc/ghi dữ liệu dạng JSON
from pathlib import Path # Import Path để làm việc với đường dẫn file

DATA_DIR = Path(__file__).parent / "data" # Trỏ tới thư mục "data" nằm cùng cấp với file này

config = { # Một dictionary chứa cấu hình mẫu
    "app_name": "OCR Pipeline", # Tên ứng dụng
    "version": "1.0", # Phiên bản
    "languages": ["vie", "eng"], # Danh sách ngôn ngữ hỗ trợ
    "ocr": {"engine": "tesseract", "dpi": 300, "preprocess": True}, # Dictionary lồng nhau chứa cấu hình OCR
}

config_path = DATA_DIR / "config.json" # Đường dẫn file JSON sẽ ghi ra
with open(config_path, "w", encoding="utf-8") as f: # Mở file ở chế độ ghi
    json.dump(config, f, indent=2, ensure_ascii=False) # Ghi dictionary thành JSON; indent=2 để xuống dòng đẹp, ensure_ascii=False để giữ tiếng Việt
print("Đã ghi:", config_path) # Thông báo đã ghi xong

with open(config_path, encoding="utf-8") as f: # Mở lại file JSON để đọc
    loaded = json.load(f) # Đọc nội dung JSON từ file và chuyển thành dictionary Python

print(loaded["app_name"]) # Truy cập giá trị của khóa "app_name"
print(loaded["ocr"]["engine"]) # Truy cập giá trị lồng nhau: trong "ocr" lấy "engine"
print(loaded["languages"]) # Truy cập danh sách ngôn ngữ

text = '{"name": "Duc", "score": 9.5, "passed": true}' # Một chuỗi JSON (lưu ý: là chuỗi, chưa phải dictionary)
data = json.loads(text) # json.loads chuyển CHUỖI JSON thành dictionary Python (loads = load string)
print(data["name"], data["score"], data["passed"]) # In các giá trị; lưu ý true trong JSON thành True trong Python

back_to_text = json.dumps(data, ensure_ascii=False) # json.dumps chuyển dictionary trở lại thành CHUỖI JSON (dumps = dump string)
print(back_to_text) # In ra chuỗi JSON

students = [ # Danh sách các sinh viên, mỗi sinh viên là một dictionary
    {"name": "An", "scores": {"python": 8, "sql": 7}}, # Sinh viên An với điểm các môn
    {"name": "Binh", "scores": {"python": 9, "sql": 8}}, # Sinh viên Binh với điểm các môn
]
for s in students: # Duyệt qua từng sinh viên
    avg = sum(s["scores"].values()) / len(s["scores"]) # Tính điểm trung bình: tổng các điểm chia cho số môn
    print(f"{s['name']}: điểm trung bình {avg:.1f}") # In tên và điểm trung bình (1 chữ số thập phân)
