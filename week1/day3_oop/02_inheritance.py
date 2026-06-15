class Animal: # Lớp cha (base class) đại diện cho động vật nói chung
    def __init__(self, name): # Hàm khởi tạo, nhận vào tên của con vật
        self.name = name # Lưu tên vào thuộc tính name

    def speak(self): # Phương thức phát ra âm thanh - sẽ được lớp con ghi đè (override)
        return f"{self.name} phát ra âm thanh" # Hành vi mặc định của Animal


class Dog(Animal): # Lớp Dog kế thừa (inherit) từ Animal - tự động có thuộc tính name
    def speak(self): # Ghi đè (override) phương thức speak của lớp cha
        return f"{self.name} sủa: Gâu gâu!" # Chó có cách phát âm thanh riêng


class Cat(Animal): # Lớp Cat cũng kế thừa từ Animal
    def speak(self): # Ghi đè phương thức speak
        return f"{self.name} kêu: Meo meo!" # Mèo có cách phát âm thanh riêng


class Puppy(Dog): # Lớp Puppy kế thừa từ Dog (kế thừa nhiều tầng: Puppy -> Dog -> Animal)
    def speak(self): # Ghi đè phương thức speak
        base = super().speak() # Gọi phương thức speak của lớp cha (Dog) để tái sử dụng
        return base + " (giọng nhỏ xíu)" # Thêm phần mô tả riêng vào kết quả của lớp cha


animals = [Dog("Rex"), Cat("Mun"), Puppy("Bun"), Animal("Bí ẩn")] # Danh sách chứa nhiều object thuộc các lớp khác nhau
for animal in animals: # Duyệt qua từng con vật trong danh sách
    print(animal.speak()) # Gọi speak() - mỗi object tự gọi đúng phiên bản của mình (tính đa hình - polymorphism)

print(isinstance(animals[0], Animal)) # Kiểm tra object đầu tiên (Dog) có phải là Animal không -> True (vì Dog kế thừa Animal)
print(issubclass(Puppy, Animal)) # Kiểm tra lớp Puppy có phải là lớp con của Animal không -> True


class Document: # Lớp cha đại diện cho một tài liệu
    def __init__(self, path): # Hàm khởi tạo nhận đường dẫn tới file
        self.path = path # Lưu đường dẫn vào thuộc tính path

    def extract_text(self): # Phương thức trích xuất văn bản - bắt buộc lớp con phải tự cài đặt
        raise NotImplementedError("Lớp con phải tự cài đặt extract_text") # Ném lỗi nếu lớp con quên cài đặt


class PdfDocument(Document): # Lớp xử lý tài liệu PDF, kế thừa từ Document
    def extract_text(self): # Cài đặt cách trích xuất text riêng cho PDF
        return f"Trích xuất text từ PDF: {self.path}" # Mô phỏng việc đọc text từ PDF


class ImageDocument(Document): # Lớp xử lý tài liệu ảnh, kế thừa từ Document
    def extract_text(self): # Cài đặt cách trích xuất text riêng cho ảnh
        return f"Chạy OCR trên ảnh: {self.path}" # Mô phỏng việc dùng OCR để đọc chữ từ ảnh


docs = [PdfDocument("report.pdf"), ImageDocument("scan.png")] # Danh sách các tài liệu thuộc loại khác nhau
for doc in docs: # Duyệt qua từng tài liệu
    print(doc.extract_text()) # Mỗi tài liệu tự dùng cách trích xuất phù hợp của mình
