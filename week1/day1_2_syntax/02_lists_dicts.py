fruits = ["apple", "banana", "orange"] # Danh sách (list) các loại trái cây
fruits.append("mango") # Thêm "mango" vào cuối danh sách
fruits.insert(1, "grape") # Chèn "grape" vào vị trí index 1 (sau "apple")
fruits.remove("banana") # Xóa "banana" khỏi danh sách
print(fruits) # Kết quả: ['apple', 'grape', 'orange', 'mango']
print(fruits[0], fruits[-1]) # Truy cập phần tử đầu tiên (index 0) và phần tử cuối cùng (index -1)
print(fruits[1:3]) # Lấy một phần của danh sách từ index 1 đến index 2 (không bao gồm index 3)
print(sorted(fruits)) # Sắp xếp danh sách theo thứ tự chữ cái, nhưng không thay đổi danh sách gốc
print(fruits) # Kết quả vẫn là: ['apple', 'grape', '

numbers = [5, 2, 9, 1, 7]
print(sum(numbers), max(numbers), min(numbers)) # Tính tổng, giá trị lớn nhất và nhỏ nhất trong danh sách numbers

squares = [n * n for n in numbers] # Tạo một danh sách mới chứa bình phương của mỗi số trong danh sách numbers bằng cách sử dụng list comprehension
print(squares)

evens = [n for n in numbers if n % 2 == 0] # Tạo một danh sách mới chứa các số chẵn trong danh sách numbers bằng cách sử dụng list comprehension với điều kiện
print(evens)

student = {
    "name": "Duc",
    "age": 27,
    "skills": ["Python", "SQL"],
} # Từ điển (dictionary) chứa thông tin về một sinh viên
print(student["name"]) # Truy cập giá trị của khóa "name" trong từ điển student
print(student.get("email", "chưa có email")) # Truy cập giá trị của khóa "email" trong từ điển student, nếu không tồn tại thì trả về "chưa có email"

student["email"] = "hongduc10111999@gmail.com" # Thêm một cặp khóa-giá trị mới vào từ điển student với khóa là "email" và giá trị là "hongduc10111999@gmail.com"
student["age"] = 28 # Cập nhật giá trị của khóa "age" trong từ điển student
print(student)

for key, value in student.items(): # Duyệt qua tất cả các cặp khóa-giá trị trong từ điển student và in ra chúng
    print(key, "->", value) 

scores = {"math": 8, "english": 7, "physics": 9}
passed = {subject: score for subject, score in scores.items() if score >= 8} # Tạo một từ điển mới chứa các môn học và điểm số của những môn có điểm số lớn hơn hoặc bằng 8 bằng cách sử dụng dictionary comprehension với điều kiện
print(passed)

point = (10, 20)
x, y = point
print(x, y)

unique_tags = {"python", "ai", "python", "ocr"}
print(unique_tags)
