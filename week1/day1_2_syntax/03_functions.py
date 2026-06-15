def greet(name): # Định nghĩa hàm greet nhận vào 1 tham số là name
    return f"Xin chào {name}!" # Trả về chuỗi chào hỏi có chèn tên


def calc_total(price, quantity=1, discount=0.0): # Hàm tính tổng tiền; quantity mặc định 1, discount mặc định 0.0 (tham số có giá trị mặc định)
    total = price * quantity # Tính tổng tiền trước giảm giá = đơn giá x số lượng
    return total * (1 - discount) # Trả về tổng tiền sau khi áp dụng giảm giá (vd: discount 0.1 = giảm 10%)


def stats(numbers): # Hàm tính thống kê cho một danh sách số
    return min(numbers), max(numbers), sum(numbers) / len(numbers) # Trả về cùng lúc 3 giá trị: nhỏ nhất, lớn nhất, trung bình (dưới dạng tuple)


def describe(*args, **kwargs): # Hàm nhận số lượng tham số tùy ý: *args gom các tham số thường, **kwargs gom các tham số có tên
    print("args:", args) # In ra các tham số không tên (dưới dạng tuple)
    print("kwargs:", kwargs) # In ra các tham số có tên (dưới dạng dictionary)


print(greet("Duc")) # Gọi hàm greet với tên "Duc"
print(calc_total(100)) # Chỉ truyền giá, quantity và discount dùng giá trị mặc định -> 100
print(calc_total(100, 3)) # Truyền giá và số lượng -> 300
print(calc_total(100, quantity=2, discount=0.1)) # Truyền tham số theo tên, có giảm giá 10% -> 180

lowest, highest, average = stats([4, 8, 15, 16, 23, 42]) # Gọi stats và tách 3 giá trị trả về vào 3 biến (giải nén tuple)
print(lowest, highest, average) # In ra giá trị nhỏ nhất, lớn nhất và trung bình

describe(1, 2, 3, name="Duc", course="AI Bootcamp") # 1,2,3 vào args; name và course vào kwargs


def apply_twice(func, value): # Hàm nhận vào MỘT HÀM khác (func) và một giá trị, rồi áp dụng hàm đó 2 lần
    return func(func(value)) # Gọi func lên value, rồi gọi func lên kết quả đó một lần nữa


def add_five(n): # Hàm đơn giản: cộng thêm 5 vào n
    return n + 5 # Trả về n + 5


print(apply_twice(add_five, 10)) # Truyền hàm add_five làm tham số: 10 -> 15 -> 20
