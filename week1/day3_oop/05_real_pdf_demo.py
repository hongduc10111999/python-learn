"""Phiên bản ĐỌC FILE THẬT của ví dụ Document trong 02_inheritance.py.

Khác với 02_inheritance.py (chỉ mô phỏng/in ra path), file này thực sự:
  - Tạo ra một file report.pdf có nội dung chữ
  - Mở file đó và trích xuất (extract) chữ ra
"""

from pathlib import Path  # Để làm việc với đường dẫn file một cách an toàn

from reportlab.pdfgen import canvas  # Thư viện tạo file PDF
from pypdf import PdfReader  # Thư viện đọc file PDF

# Thư mục chứa file demo = cùng thư mục với file .py này
HERE = Path(__file__).parent


def tao_pdf_mau(path: Path) -> None:  # Hàm tạo một file PDF thật để có cái mà đọc
    c = canvas.Canvas(str(path))  # Tạo "khung vẽ" cho file PDF
    c.drawString(100, 750, "Bao cao thang 6")  # Viết dòng chữ vào toạ độ (x=100, y=750)
    c.drawString(100, 730, "Doanh thu: 1000 USD")  # Viết thêm một dòng nữa
    c.drawString(100, 710, "Nhan vien xuat sac: Duc")  # Dòng thứ ba
    c.save()  # Lưu file xuống ổ đĩa


class Document:  # Lớp cha đại diện cho một tài liệu (giống 02_inheritance.py)
    def __init__(self, path):  # Nhận đường dẫn tới file
        self.path = path  # Lưu lại

    def extract_text(self):  # Lớp con bắt buộc tự cài đặt
        raise NotImplementedError("Lớp con phải tự cài đặt extract_text")


class PdfDocument(Document):  # Lớp xử lý PDF - LẦN NÀY ĐỌC FILE THẬT
    def extract_text(self):
        reader = PdfReader(self.path)  # Mở file PDF thật từ ổ đĩa
        # Gộp chữ từ tất cả các trang lại thành một chuỗi
        return "\n".join(page.extract_text() for page in reader.pages)


if __name__ == "__main__":
    pdf_path = HERE / "report.pdf"  # Đường dẫn file PDF sẽ tạo/đọc

    tao_pdf_mau(pdf_path)  # Bước 1: tạo file PDF thật
    print(f"Đã tạo file thật: {pdf_path}\n")

    doc = PdfDocument(str(pdf_path))  # Bước 2: tạo object trỏ tới file thật
    print("--- Nội dung trích xuất từ PDF ---")
    print(doc.extract_text())  # Bước 3: đọc chữ ra từ file
