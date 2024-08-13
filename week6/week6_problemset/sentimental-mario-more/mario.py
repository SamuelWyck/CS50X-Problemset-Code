def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            pass

    for i in range(height + 1):
        if i == 0:
            continue
        print(" " * (height - i), end="")
        print("#" * i, end="")
        print("  ", end="")
        print("#" * i)

if __name__ == "__main__":
    main()
