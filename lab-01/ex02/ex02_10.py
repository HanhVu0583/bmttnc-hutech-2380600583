def dao_nguoc_chuoi(chuoi):
    return chuoi[::-1]
input_str = input("nhap mot chuoi: ")
print("chuoi sau khi dao nguoc:", dao_nguoc_chuoi(input_str))
