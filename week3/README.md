# Tuần 3: LLM & RAG System

Mục tiêu: xây một **chatbot RAG** trả lời câu hỏi dựa trên tài liệu thật — nối tiếp output OCR của Tuần 2 (các file `*_chunks.json`).

## RAG là gì?

**RAG = Retrieval-Augmented Generation.** Thay vì hỏi thẳng LLM (dễ bịa), ta:
1. **Retrieval** — tìm các đoạn tài liệu liên quan đến câu hỏi
2. **Augmented** — đưa các đoạn đó vào prompt làm ngữ cảnh
3. **Generation** — để LLM trả lời dựa trên ngữ cảnh thật → chính xác, có trích dẫn

## Chuẩn bị: API key Gemini (miễn phí)

1. Vào https://aistudio.google.com/apikey lấy API key miễn phí (1M token/ngày)
2. Copy file mẫu và điền key:
   ```bash
   cp .env.example .env
   # mở .env, dán key vào GEMINI_API_KEY
   ```

## Cài đặt

```bash
cd week3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Lưu ý warning:** trên Python 3.9 sẽ có vài dòng `FutureWarning` (do thư viện Google khuyến nghị Python 3.10+). Đây là cảnh báo vô hại, không ảnh hưởng kết quả. Muốn ẩn hẳn thì chạy với cờ: `python -W ignore <file>.py`.

## Cấu trúc theo từng ngày

| Thư mục | Ngày | Nội dung |
|---------|------|----------|
| `day1_2_llm/` | Day 1–2 | Gọi Gemini, system prompt, few-shot, chain-of-thought |
| `day3_embeddings/` | Day 3 | Embeddings, cosine similarity, ChromaDB cơ bản |
| `day4_5_rag/` | Day 4–5 | RAG pipeline: index chunk Tuần 2 → retrieve → generate |
| `day6_7_advanced/` | Day 6–7 | Metadata filtering, reranking |
| `chatbot/` | Tổng hợp | **Deliverable**: chatbot CLI hỏi đáp có trích dẫn |

## Chạy từng phần

```bash
python day1_2_llm/01_basic_call.py        # gọi Gemini đơn giản
python day1_2_llm/02_system_prompt.py     # đóng vai trợ lý
python day1_2_llm/03_few_shot.py          # phân loại bằng ví dụ mẫu
python day1_2_llm/04_chain_of_thought.py  # suy luận từng bước

python day3_embeddings/01_embeddings.py        # biến text thành vector
python day3_embeddings/02_cosine_similarity.py # đo độ giống nhau
python day3_embeddings/03_chromadb_basic.py    # lưu & tìm trong Vector DB

python day4_5_rag/indexer.py   # nạp chunk Tuần 2 vào ChromaDB
python day4_5_rag/rag.py       # hỏi đáp RAG hoàn chỉnh

python day6_7_advanced/01_metadata_filter.py
python day6_7_advanced/02_reranking.py
```

## Deliverable cuối tuần

```bash
python chatbot/chat.py
```

Chatbot CLI: tự động index chunk từ Tuần 2 (lần đầu) → nhận câu hỏi → tìm ngữ cảnh → trả lời kèm nguồn. Gõ `exit` để thoát.

**Yêu cầu trước khi chạy:** đã có file `week2/output/*_chunks.json` (chạy pipeline OCR Tuần 2). Nếu chưa có, vào `week2` chạy `python ocr_pipeline/pipeline.py`.

## Luồng hoạt động (RAG)

```
Câu hỏi
   │
   ▼
[embed câu hỏi thành vector]
   │
   ▼
[tìm trong ChromaDB top-k chunk gần nghĩa nhất]  ← Retrieval
   │
   ▼
[ghép câu hỏi + chunk thành prompt]              ← Augmented
   │
   ▼
[Gemini sinh câu trả lời từ ngữ cảnh]            ← Generation
   │
   ▼
Câu trả lời + nguồn trích dẫn
```

**Tiêu chí hoàn thành:** chatbot nhận câu hỏi → tìm đúng ngữ cảnh trong tài liệu → trả lời chính xác, và nói "không tìm thấy" khi tài liệu không có thông tin (không bịa).

## Cấu trúc thư mục

```
week3/
├── config.py              # nạp API key, khởi tạo Gemini (dùng chung)
├── chroma_db/             # database vector (tự tạo khi index)
├── day1_2_llm/            # Day 1–2 — LLM & prompt
├── day3_embeddings/       # Day 3 — embeddings & vector DB
├── day4_5_rag/            # Day 4–5 — RAG pipeline
├── day6_7_advanced/       # Day 6–7 — kỹ thuật nâng cao
├── chatbot/               # Deliverable
├── .env.example           # mẫu file cấu hình
└── requirements.txt
```
