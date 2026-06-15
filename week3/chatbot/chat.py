import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import require_api_key
from day4_5_rag.indexer import get_collection, index_chunks
from day4_5_rag.rag import answer


def ensure_indexed():
    collection = get_collection()
    if collection.count() == 0:
        print("Chưa có dữ liệu, đang index các chunk từ Tuần 2...")
        n = index_chunks()
        print(f"Đã index {n} chunk.\n")
    else:
        print(f"Đã có {collection.count()} chunk trong kho.\n")


def main():
    require_api_key()
    print("=== RAG Chatbot (Tuần 3) ===")
    print("Hỏi đáp dựa trên tài liệu đã OCR ở Tuần 2.")
    print("Gõ 'exit' để thoát.\n")

    ensure_indexed()

    while True:
        try:
            query = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTạm biệt!")
            break
        if query.lower() in {"exit", "quit", "thoat"}:
            print("Tạm biệt!")
            break
        if not query:
            continue

        reply, chunks = answer(query)
        print(f"\nBot: {reply}")
        sources = sorted({c["source"] for c in chunks})
        print(f"📎 Nguồn: {', '.join(sources)}\n")


if __name__ == "__main__":
    main()
