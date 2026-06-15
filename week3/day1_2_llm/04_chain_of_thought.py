import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_MODEL, require_api_key

require_api_key()

QUESTION = """Một cửa hàng bán 3 laptop giá 1200 USD mỗi chiếc, 2 màn hình giá 310 USD
mỗi chiếc. Khách được giảm 10% tổng đơn. Hỏi khách phải trả bao nhiêu?"""


def ask_direct(question):
    model = genai.GenerativeModel(GEMINI_MODEL)
    return model.generate_content(question + "\nChỉ trả lời con số cuối cùng.").text


def ask_cot(question):
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = question + "\nHãy suy luận từng bước rồi mới đưa ra đáp án cuối cùng."
    return model.generate_content(prompt).text


if __name__ == "__main__":
    print("=== Trả lời thẳng (không suy luận) ===")
    print(ask_direct(QUESTION))

    print("\n=== Chain-of-thought (suy luận từng bước) ===")
    print(ask_cot(QUESTION))
