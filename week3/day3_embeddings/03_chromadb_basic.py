import sys
from pathlib import Path

import chromadb
import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EMBEDDING_MODEL, require_api_key

require_api_key()


def embed(text, task_type="retrieval_document"):
    return genai.embed_content(
        model=EMBEDDING_MODEL, content=text, task_type=task_type
    )["embedding"]


def build_demo_collection():
    client = chromadb.Client()
    collection = client.create_collection("demo")

    docs = [
        "Laptop Dell XPS giá 1200 USD, còn hàng.",
        "Chuột Logitech không dây giá 25 USD.",
        "Màn hình LG 27 inch độ phân giải 4K.",
        "Bảo hành sản phẩm điện tử 12 tháng.",
    ]
    collection.add(
        ids=[f"doc-{i}" for i in range(len(docs))],
        documents=docs,
        embeddings=[embed(d) for d in docs],
    )
    return collection


def search(collection, query, top_k=2):
    query_vec = embed(query, task_type="retrieval_query")
    return collection.query(query_embeddings=[query_vec], n_results=top_k)


if __name__ == "__main__":
    collection = build_demo_collection()
    print("Đã thêm 4 tài liệu vào ChromaDB\n")

    query = "laptop giá bao nhiêu?"
    results = search(collection, query, top_k=2)
    print(f"Câu hỏi: {query}")
    print("Top 2 tài liệu gần nhất:")
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        print(f"  (khoảng cách {dist:.3f}) {doc}")
