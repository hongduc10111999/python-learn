import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import require_api_key
from day4_5_rag.indexer import embed, get_collection

require_api_key()


def search_in_source(query, source, top_k=3):
    collection = get_collection()
    query_vec = embed(query, task_type="retrieval_query")
    return collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        where={"source": source},
    )


if __name__ == "__main__":
    query = "sản phẩm và giá"
    source = "report.pdf"
    print(f"Tìm '{query}' CHỈ trong tài liệu '{source}':\n")
    results = search_in_source(query, source)
    for doc in results["documents"][0]:
        print(f"  - {doc[:60]}...")
    print("\n=> metadata filter giúp giới hạn tìm kiếm trong 1 tài liệu cụ thể")
