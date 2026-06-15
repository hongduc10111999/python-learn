import sys
from pathlib import Path

import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_MODEL, require_api_key
from day4_5_rag.indexer import embed, get_collection

RAG_SYSTEM_PROMPT = """Bạn là trợ lý trả lời câu hỏi dựa trên TÀI LIỆU được cung cấp.
Quy tắc:
- Chỉ trả lời dựa vào nội dung trong phần NGỮ CẢNH bên dưới.
- Nếu ngữ cảnh không có thông tin, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu."
- Trả lời ngắn gọn bằng tiếng Việt và ghi rõ nguồn (source) đã dùng.
"""


def retrieve(query, top_k=3):
    collection = get_collection()
    query_vec = embed(query, task_type="retrieval_query")
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": doc, "source": meta.get("source", "?")})
    return chunks


def build_prompt(query, chunks):
    context = "\n\n".join(
        f"[Nguồn: {c['source']}]\n{c['text']}" for c in chunks
    )
    return f"NGỮ CẢNH:\n{context}\n\nCÂU HỎI: {query}"


def answer(query, top_k=3):
    require_api_key()
    chunks = retrieve(query, top_k=top_k)
    prompt = build_prompt(query, chunks)
    model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=RAG_SYSTEM_PROMPT)
    response = model.generate_content(prompt)
    return response.text, chunks


if __name__ == "__main__":
    questions = [
        "Có những sản phẩm nào trong báo cáo?",
        "Đơn hàng 1001 là sản phẩm gì, giá bao nhiêu?",
        "Thủ đô nước Pháp là gì?",
    ]
    for q in questions:
        print(f"\n{'='*60}\nCÂU HỎI: {q}")
        reply, chunks = answer(q)
        print(f"\nTRẢ LỜI: {reply}")
        print(f"\nĐã dùng {len(chunks)} chunk:")
        for c in chunks:
            print(f"  - [{c['source']}] {c['text'][:50]}...")
