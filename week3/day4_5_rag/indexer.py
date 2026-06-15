import json
import sys
from pathlib import Path

import chromadb
import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CHROMA_DIR, EMBEDDING_MODEL, require_api_key

CHUNKS_DIR = Path(__file__).parent.parent.parent / "week2" / "output"
COLLECTION_NAME = "documents"


def embed(text, task_type="retrieval_document"):
    return genai.embed_content(
        model=EMBEDDING_MODEL, content=text, task_type=task_type
    )["embedding"]


def load_chunks():
    records = []
    for json_file in CHUNKS_DIR.glob("*_chunks.json"):
        with open(json_file, encoding="utf-8") as f:
            records.extend(json.load(f))
    return records


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(COLLECTION_NAME)


def index_chunks():
    require_api_key()
    records = load_chunks()
    if not records:
        raise SystemExit(
            f"Không tìm thấy chunk nào trong {CHUNKS_DIR}.\n"
            "Hãy chạy pipeline OCR ở Tuần 2 trước để tạo file *_chunks.json."
        )

    collection = get_collection()
    collection.add(
        ids=[r["id"] for r in records],
        documents=[r["text"] for r in records],
        embeddings=[embed(r["text"]) for r in records],
        metadatas=[{"source": r["source"]} for r in records],
    )
    return len(records)


if __name__ == "__main__":
    n = index_chunks()
    print(f"Đã index {n} chunk vào ChromaDB tại {CHROMA_DIR}")
