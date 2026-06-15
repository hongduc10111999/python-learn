import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_MODEL, require_api_key

require_api_key()


def ask(prompt):
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    print("=== Gọi Gemini đơn giản ===")
    print(ask("Giải thích RAG trong 2 câu, dễ hiểu cho người mới."))

    print("\n=== Câu hỏi khác ===")
    print(ask("Liệt kê 3 bước chính của một hệ thống RAG."))
