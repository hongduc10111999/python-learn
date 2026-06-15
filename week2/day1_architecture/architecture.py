from dataclasses import dataclass, field


@dataclass
class Container:
    name: str
    technology: str
    responsibility: str


CONTAINERS = [
    Container("Chat UI", "Streamlit", "Nhận câu hỏi và file từ người dùng, hiển thị câu trả lời + trích dẫn"),
    Container("API Gateway", "FastAPI", "Điều phối: nhận request, gọi OCR và Query Engine, trả kết quả"),
    Container("OCR Pipeline", "Tesseract / EasyOCR", "Trích xuất text từ ảnh và PDF"),
    Container("Vector DB", "ChromaDB", "Lưu embedding các đoạn text, tìm theo độ tương đồng"),
    Container("Query Engine", "LangChain", "Chunk, embed, retrieve top-k, ghép prompt + context"),
    Container("LLM", "Gemini / Groq", "Sinh câu trả lời từ context lấy được"),
]

INGEST_FLOW = [
    "User upload tài liệu (PDF/ảnh) qua Chat UI",
    "API Gateway nhận file, đẩy sang OCR Pipeline",
    "OCR Pipeline trích text thô",
    "Query Engine làm sạch và chunk text",
    "Mỗi chunk được embed thành vector",
    "Vector + metadata được index vào Vector DB",
]

QUERY_FLOW = [
    "User gửi câu hỏi qua Chat UI",
    "API Gateway chuyển câu hỏi sang Query Engine",
    "Query Engine embed câu hỏi, truy vấn Vector DB lấy top-k chunk liên quan",
    "Ghép câu hỏi + các chunk thành prompt",
    "Gửi prompt sang LLM để sinh câu trả lời",
    "Trả câu trả lời kèm trích dẫn về Chat UI",
]


def print_flow(title, steps):
    print(title)
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print()


if __name__ == "__main__":
    print("=== CÁC CONTAINER (C4 Container Model) ===")
    for c in CONTAINERS:
        print(f"[{c.technology}] {c.name}")
        print(f"    -> {c.responsibility}")
    print()
    print_flow("=== LUỒNG NẠP TÀI LIỆU (Ingest) ===", INGEST_FLOW)
    print_flow("=== LUỒNG HỎI ĐÁP (Query) ===", QUERY_FLOW)


