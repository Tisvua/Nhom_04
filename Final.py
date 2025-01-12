import pandas as pd
from itertools import permutations
# Tạo DataFrame 
data = {
    "Process": [],
    "Max_A": [],
    "Max_B": [],
    "Max_C": [],
    "Max_D": [],
    "Allocation_A": [],
    "Allocation_B": [],
    "Allocation_C": [],
    "Allocation_D": []
}

# Hàm để kiểm tra dữ liệu đầu vào hợp lệ
def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Giá trị không hợp lệ! Vui lòng nhập một số nguyên.")

# Nhập dữ liệu 
num_processes = get_int_input("Nhập số lượng tiến trình: ")

for i in range(num_processes):
    process = f"P{i + 1}"  # Tạo tên tiến trình tự động
    print(f"Nhập dữ liệu cho tiến trình {process}:")
    max_a = get_int_input(f"  Nhập Max A: ")
    max_b = get_int_input(f"  Nhập Max B: ")
    max_c = get_int_input(f"  Nhập Max C: ")
    max_d = get_int_input(f"  Nhập Max D: ")
    alloc_a = get_int_input(f"  Nhập Allocation A: ")
    alloc_b = get_int_input(f"  Nhập Allocation B: ")
    alloc_c = get_int_input(f"  Nhập Allocation C: ")
    alloc_d = get_int_input(f"  Nhập Allocation D: ")
    
    # Cập nhật dữ liệu vào DataFrame
    data["Process"].append(process)
    data["Max_A"].append(max_a)
    data["Max_B"].append(max_b)
    data["Max_C"].append(max_c)
    data["Max_D"].append(max_d)
    data["Allocation_A"].append(alloc_a)
    data["Allocation_B"].append(alloc_b)
    data["Allocation_C"].append(alloc_c)
    data["Allocation_D"].append(alloc_d)

# Nhập giá trị cho bảng Available
print("\nNhập dữ liệu cho bảng Available:")
available_a = get_int_input("  Nhập Available A: ")
available_b = get_int_input("  Nhập Available B: ")
available_c = get_int_input("  Nhập Available C: ")
available_d = get_int_input("  Nhập Available D: ")

# Tạo DataFrame từ dữ liệu đã nhập
df = pd.DataFrame(data)

# Tạo DataFrame cho Available
available_data = {
    "Available_A": [available_a],
    "Available_B": [available_b],
    "Available_C": [available_c],
    "Available_D": [available_d]
}
available_df = pd.DataFrame(available_data)

# Tính toán bảng Need
df["Need_A"] = df["Max_A"] - df["Allocation_A"]
df["Need_B"] = df["Max_B"] - df["Allocation_B"]
df["Need_C"] = df["Max_C"] - df["Allocation_C"]
df["Need_D"] = df["Max_D"] - df["Allocation_D"]

# Hàm kiểm tra trạng thái an toàn
def is_safe_state(available, allocation, need):
    work = available.copy()
    finish = [False] * len(allocation)
    safe_sequence = []

    while len(safe_sequence) < len(allocation):
        found = False
        for i in range(len(allocation)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                for j in range(len(work)):
                    work[j] += allocation[i][j]
                safe_sequence.append(i)
                finish[i] = True
                found = True
                break
        if not found:
            return False, []

    return True, safe_sequence

# Chuyển đổi dữ liệu DataFrame thành danh sách để dễ xử lý
allocation = df[["Allocation_A", "Allocation_B", "Allocation_C", "Allocation_D"]].values.tolist()
need = df[["Need_A", "Need_B", "Need_C", "Need_D"]].values.tolist()
available = [available_a, available_b, available_c, available_d]

# Kiểm tra trạng thái an toàn
is_safe, safe_sequence = is_safe_state(available, allocation, need)

# Định dạng xuất 
print("\nMax")
print(df[["Process", "Max_A", "Max_B", "Max_C", "Max_D"]].to_string(index=False, header=["", "A", "B", "C", "D"]))

print("\nAllocations")
print(df[["Process", "Allocation_A", "Allocation_B", "Allocation_C", "Allocation_D"]].to_string(index=False, header=["", "A", "B", "C", "D"]))

print("\nAvailable")
print(available_df.to_string(index=False, header=["A", "B", "C", "D"]))

print("\nNeed")
print(df[["Process", "Need_A", "Need_B", "Need_C", "Need_D"]].to_string(index=False, header=["", "A", "B", "C", "D"]))

    
# Cập nhật hàm kiểm tra tất cả các chuỗi an toàn

def find_all_safe_sequences(available, allocation, need):
    processes = list(range(len(allocation)))
    all_safe_sequences = []

    for perm in permutations(processes):
        work = available.copy()
        finish = [False] * len(allocation)
        safe_sequence = []
        valid = True

        for i in perm:
            if all(need[i][j] <= work[j] for j in range(len(work))):
                for j in range(len(work)):
                    work[j] += allocation[i][j]
                safe_sequence.append(i)
                finish[i] = True
            else:
                valid = False
                break

        if valid and all(finish):
            all_safe_sequences.append([f"P{i+1}" for i in safe_sequence])

    return all_safe_sequences

# Chuyển đổi dữ liệu DataFrame
allocation = df[["Allocation_A", "Allocation_B", "Allocation_C", "Allocation_D"]].values.tolist()
available = [available_a, available_b, available_c, available_d]
need = df[["Need_A", "Need_B", "Need_C", "Need_D"]].values.tolist()

# Tìm tất cả các chuỗi an toàn
all_safe_sequences = find_all_safe_sequences(available, allocation, need)

if all_safe_sequences:
    print("\nHệ thống đang ở trạng thái an toàn.")
    print("Tất cả các chuỗi an toàn có thể có là:")
    for seq in all_safe_sequences:
        print(" -> ".join(seq))
else:
    print("\nHệ thống đang ở trạng thái không an toàn.")