import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_MODEL, require_api_key

require_api_key()

SYSTEM_PROMPT = """Bạn là trợ lý hỗ trợ khách hàng của một cửa hàng điện tử.
- Luôn trả lời ngắn gọn, lịch sự bằng tiếng Việt.
- Nếu không biết, nói thẳng là không biết, không bịa.
- Luôn xưng "shop" và gọi khách là "bạn".
"""


def ask(question):
    model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=SYSTEM_PROMPT)
    return model.generate_content(question).text


if __name__ == "__main__":
    print("=== Có system prompt (đóng vai trợ lý cửa hàng) ===")
    for q in [
        "Cửa hàng có bán laptop không?",
        "Thủ đô nước Pháp là gì?",
    ]:
        print(f"\nKhách: {q}")
        print(f"Bot: {ask(q)}")
