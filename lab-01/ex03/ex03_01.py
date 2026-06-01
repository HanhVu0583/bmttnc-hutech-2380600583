def tinh_tong_so_chan(lst):
    tong = 0
    for i in lst:
        if i % 2 == 0:
            tong += i
    return tong
input_list = input(" nhap cac so , cach nhau bang dau phay:")
numbers = list(map(int, input_list.split(",")))
tong_chan = tinh_tong_so_chan(numbers)
print("tong cac so chan la:", tong_chan)