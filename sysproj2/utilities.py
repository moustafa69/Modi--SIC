def add_hex(num1, num2):
    sum = hex(int(num1, 16) + int(num2, 16))
    return sum[2:].upper()


