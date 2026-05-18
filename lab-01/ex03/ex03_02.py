def dao_nguoc_list(lst):
    return lst[::-1]    
input_list = input(" nhap cac so , cach nhau bang dau phay:")
numbers = list(map(int, input_list.split(",")))
list_dao_nguoc = dao_nguoc_list(numbers)
print("list dao nguoc la:", list_dao_nguoc)