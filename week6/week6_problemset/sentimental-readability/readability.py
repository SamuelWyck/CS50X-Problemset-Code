def main():

    text = input("Text: ").lower().strip()

    letters = 0
    for c in text:
        if c.isalpha():
            letters += 1

    words = 1
    for c in text:
        if c.isspace():
            words += 1

    sentences = 0
    for c in text:
        if c.find(".") != -1 or c.find("!") != -1 or c.find("?") != -1:
            sentences += 1

    grade = liau(words, letters, sentences)

    if grade < 1:
        print("Before Grade 1")
    elif grade>= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def liau(words, letters, sentences):

    L = (letters/words) * 100
    S = (sentences/words) * 100

    index = (0.0588 * L) - (0.296 * S) - 15.8

    return round(index)






if __name__ == "__main__":
    main()
