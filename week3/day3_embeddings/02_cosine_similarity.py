import sys
from pathlib import Path

import google.generativeai as genai
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EMBEDDING_MODEL, require_api_key

require_api_key()


def embed(text):
    return genai.embed_content(model=EMBEDDING_MODEL, content=text)["embedding"]


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


if __name__ == "__main__":
    anchor = "Giá của chiếc laptop là bao nhiêu?"
    candidates = [
        "Laptop Dell XPS có giá 1200 USD",
        "Con mèo đang ngủ trên ghế sofa",
        "Máy tính xách tay này bán với giá 1200 đô",
    ]

    anchor_vec = embed(anchor)
    print(f"Câu gốc: {anchor}\n")
    scored = []
    for c in candidates:
        score = cosine_similarity(anchor_vec, embed(c))
        scored.append((score, c))

    for score, c in sorted(scored, reverse=True):
        print(f"  {score:.3f}  {c}")
    print("\n=> Điểm càng cao nghĩa là càng gần nghĩa với câu gốc")
