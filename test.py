# quotient = 5
# binary = ''
# while quotient != 0:
#     binary = str(quotient % 2) + binary
#     quotient = quotient // 2
# print(binary)

nums = [5, 31, 15, 7, 3, 2]
bicar_lst = []
for num in nums:
    bicar = 0
    quotient = num
    while quotient != 0:
        bicar += quotient % 2
        quotient //= 2
    bicar_lst.append(bicar)
print(bicar_lst)

abbcccb
