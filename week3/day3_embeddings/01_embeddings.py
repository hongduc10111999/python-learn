import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EMBEDDING_MODEL, require_api_key

require_api_key()


def embed(text):
    result = genai.embed_content(model=EMBEDDING_MODEL, content=text)
    return result["embedding"]


if __name__ == "__main__":
    text = "Laptop Dell XPS giá 1200 USD"
    vector = embed(text)
    print(f"Câu: {text}")
    print(f"Số chiều của vector: {len(vector)}")
    print(f"5 giá trị đầu: {vector[:5]}")
