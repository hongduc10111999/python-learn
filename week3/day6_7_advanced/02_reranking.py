import sys
from pathlib import Path

import google.generativeai as genai
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EMBEDDING_MODEL, require_api_key
from day4_5_rag.indexer import embed, get_collection

require_api_key()


def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve_then_rerank(query, fetch_k=6, top_k=3):
    collection = get_collection()
    query_vec = embed(query, task_type="retrieval_query")
    results = collection.query(query_embeddings=[query_vec], n_results=fetch_k)

    docs = results["documents"][0]
    reranked = []
    for doc in docs:
        score = cosine(query_vec, embed(doc, task_type="retrieval_query"))
        reranked.append((score, doc))
    reranked.sort(reverse=True)
    return reranked[:top_k]


if __name__ == "__main__":
    query = "laptop giá bao nhiêu"
    print(f"Câu hỏi: {query}")
    print(f"\nLấy 6 kết quả rồi rerank, giữ top 3:\n")
    for score, doc in retrieve_then_rerank(query):
        print(f"  {score:.3f}  {doc[:55]}...")
