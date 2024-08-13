def main():
    while True:
        try:
            number = int(input("How many times? "))
            break
        except ValueError:
            continue

    meow(number)

def meow(times=1):
    for _ in range(times):
        print("meow")

if __name__ == "__main__":
    main()
