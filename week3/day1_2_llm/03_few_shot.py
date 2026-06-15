import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_MODEL, require_api_key

require_api_key()

FEW_SHOT_PROMPT = """Phân loại cảm xúc của câu thành: TÍCH CỰC, TIÊU CỰC, hoặc TRUNG TÍNH.

Câu: "Sản phẩm tuyệt vời, giao hàng nhanh!"
Cảm xúc: TÍCH CỰC

Câu: "Hàng lỗi, thất vọng quá."
Cảm xúc: TIÊU CỰC

Câu: "Đơn hàng đã được giao lúc 3 giờ chiều."
Cảm xúc: TRUNG TÍNH

Câu: "{review}"
Cảm xúc:"""


def classify(review):
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = FEW_SHOT_PROMPT.format(review=review)
    return model.generate_content(prompt).text.strip()


if __name__ == "__main__":
    print("=== Few-shot: dạy model bằng vài ví dụ mẫu ===")
    for review in [
        "Mình rất hài lòng với chiếc tai nghe này!",
        "Pin tụt nhanh, không như quảng cáo.",
        "Máy có màu đen và trắng.",
    ]:
        print(f"\nĐánh giá: {review}")
        print(f"Phân loại: {classify(review)}")
