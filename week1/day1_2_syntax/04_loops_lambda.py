for i in range(5): # Lặp với i lần lượt nhận các giá trị 0, 1, 2, 3, 4 (range(5) tạo dãy từ 0 đến 4)
    print("vòng lặp thứ", i) # In ra số thứ tự của vòng lặp

for i in range(1, 10, 2): # Lặp từ 1 đến 9, bước nhảy 2 (1, 3, 5, 7, 9)
    print(i, end=" ") # In trên cùng một dòng, cách nhau bằng dấu cách (end=" " thay vì xuống dòng)
print() # In một dòng trống để xuống dòng

count = 3 # Khởi tạo biến đếm bằng 3
while count > 0: # Vòng lặp while: lặp lại chừng nào count vẫn lớn hơn 0
    print("đếm ngược:", count) # In giá trị hiện tại của count
    count -= 1 # Giảm count đi 1 mỗi vòng (tránh lặp vô hạn)

for n in range(10): # Lặp n từ 0 đến 9
    if n == 3: # Khi n bằng 3
        continue # Bỏ qua phần còn lại của vòng này, nhảy sang vòng tiếp theo (số 3 không được in)
    if n == 6: # Khi n bằng 6
        break # Thoát hẳn khỏi vòng lặp (dừng tại đây, không in 6 trở đi)
    print(n, end=" ") # In n trên cùng dòng (kết quả: 0 1 2 4 5)
print() # Xuống dòng

products = ["laptop", "mouse", "keyboard"] # Danh sách các sản phẩm
for index, item in enumerate(products, start=1): # enumerate vừa lấy chỉ số vừa lấy giá trị; start=1 để đếm từ 1 thay vì 0
    print(index, item) # In số thứ tự kèm tên sản phẩm

prices = [1000, 20, 50] # Danh sách giá tương ứng với từng sản phẩm
for item, price in zip(products, prices): # zip ghép từng cặp phần tử của 2 danh sách lại với nhau
    print(f"{item}: ${price}") # In tên sản phẩm cùng giá của nó

double = lambda x: x * 2 # lambda là hàm ẩn danh (viết gọn 1 dòng): nhận x, trả về x*2
print(double(21)) # Gọi hàm lambda với 21 -> 42

nums = [3, 1, 4, 1, 5, 9, 2, 6] # Danh sách các số
print(sorted(nums, key=lambda n: -n)) # Sắp xếp; key=lambda n: -n để sắp theo thứ tự GIẢM DẦN (dùng dấu âm)

people = [ # Danh sách người, mỗi người là một dictionary
    {"name": "An", "age": 30}, # Người tên An, 30 tuổi
    {"name": "Binh", "age": 22}, # Người tên Binh, 22 tuổi
    {"name": "Chi", "age": 27}, # Người tên Chi, 27 tuổi
]
people.sort(key=lambda p: p["age"]) # Sắp xếp danh sách theo tuổi tăng dần (key chỉ định sắp theo trường "age")
print(people) # In danh sách đã sắp xếp theo tuổi

doubled = list(map(lambda n: n * 2, nums)) # map áp dụng hàm lambda (nhân đôi) lên TỪNG phần tử của nums
big = list(filter(lambda n: n > 4, nums)) # filter giữ lại CHỈ những phần tử thỏa điều kiện (lớn hơn 4)
print(doubled) # In danh sách đã nhân đôi
print(big) # In danh sách các số lớn hơn 4
