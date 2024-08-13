def main():

    while True:
        card_number = input("Number: ")
        if card_number.isdigit():
            break

    if not 13 <= len(card_number) <= 16:
        print("INVALID")
    elif check(card_number) == False:
        print("INVALID")
    elif card_number[:2] == "34" or card_number[:2] == "37":
        print("AMEX")
    elif 51 <= int(card_number[:2]) <= 55:
        print("MASTERCARD")
    elif card_number[:1] == "4":
        print("VISA")
    else:
        print("INVALID")


def check(number):
    digits = []
    odd_digits = []
    even_digits = []

    for num in number:
        digits.append(num)

    index = len(digits) - 2
    while index >= 0:
        odd_digits.append(digits[index])
        index -= 2

    dex = len(digits) - 1
    while dex >= 0:
        even_digits.append(digits[dex])
        dex -= 2

    for i in range(len(odd_digits)):
        odd_digits[i] = str(int(odd_digits[i]) * 2)

    odd = "".join(odd_digits)

    odd_sum = 0
    for n in odd:
        odd_sum = odd_sum + int(n)

    sum_even = eval("+".join(even_digits))

    sum = str(sum_even + odd_sum)

    if sum[len(sum)-1:] == "0":
        return True
    else:
        return False

if __name__ == "__main__":
    main()
