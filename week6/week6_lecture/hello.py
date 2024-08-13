
while True:
    answer = input("What's your name? ")
    if answer.isalpha() == False:
        continue
    else:
        break

print(f"hello, {answer}")
