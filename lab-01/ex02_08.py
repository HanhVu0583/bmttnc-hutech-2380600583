def chia_het_cho_5(so_nhi_phan):
    so_nhi_phan = int(so_nhi_phan, 2)
    if so_nhi_phan % 5 == 0:
        return True
    else:
        return False
chuoi_nhi_phan = input("nhap chuoi so nhi phan: ")
so_nhi_phan = chuoi_nhi_phan.strip()
so_chia_het_cho_5 = [so for so in so_nhi_phan.split(',') if chia_het_cho_5(so)]
if so_chia_het_cho_5>0:
    ket_qua = ','.join(so_chia_het_cho_5)
    print("cac so nhi phan chia het cho 5 la:", ket_qua)
else:    print("khong co so nhi phan nao chia het cho 5.")  