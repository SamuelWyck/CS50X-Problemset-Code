while True:
    x = input("x: ")
    y = input("y: ")
    if x.isdigit() == False or y.isdigit() == False:
        continue
    else:
        z = int(x) / int(y)
        break

print(f"{z}")
