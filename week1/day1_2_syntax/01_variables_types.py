name = "Duc"
age = 27
height = 1.76
is_learning = True

print(name, type(name)) # Chuỗi (string)
print(age, type(age)) # Số nguyên (integer)
print(height, type(height)) # Số thực (float)
print(is_learning, type(is_learning)) # Boolean (True/False)

greeting = f"Xin chào {name}, năm sau bạn {age + 1} tuổi"
print(greeting)

text = "AI Training Bootcamp"
print(text.lower()) # Chuyển tất cả ký tự thành chữ thường
print(text.upper()) # Chuyển tất cả ký tự thành chữ hoa
print(text.replace("Bootcamp", "Course")) # Thay thế "Bootcamp" bằng "Course"
print(text.split(" ")) # Tách chuỗi thành danh sách các từ
print(len(text)) # Độ dài của chuỗi
print("Training" in text) # Kiểm tra xem "Training" có trong text không

x = "100"
y = int(x) + 50 # Chuyển x từ chuỗi sang số nguyên để có thể cộng với 50
print(y)

price = 19.99
print(f"Giá: {price:.1f}") # 1 chữ số thập phân
print(f"Giá: {price:>10.2f}") # 10: tổng độ rộng, .2f: 2 chữ số thập phân, >: căn phải
