def clean(text): # Hàm làm sạch chuỗi: xóa khoảng trắng thừa
    return " ".join(text.split()).strip() # split() tách chuỗi theo khoảng trắng (bỏ khoảng trắng thừa), join nối lại bằng 1 dấu cách, strip() xóa khoảng trắng đầu/cuối


def word_count(text): # Hàm đếm số từ trong chuỗi
    return len(clean(text).split()) # Làm sạch chuỗi trước, rồi tách thành danh sách từ và đếm độ dài


def truncate(text, max_length=20): # Hàm cắt ngắn chuỗi nếu vượt quá độ dài cho phép (mặc định 20 ký tự)
    if len(text) <= max_length: # Nếu chuỗi đã đủ ngắn
        return text # Giữ nguyên, trả về luôn
    return text[: max_length - 3] + "..." # Cắt lấy phần đầu và thêm "..." (trừ 3 ký tự để chừa chỗ cho dấu chấm)
