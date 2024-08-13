words = set()

def check(word):
    if word.lower() in words:
        return True

def load(dictionary):
    with open(dictionary) as file:
        words.update(file.read().splitlines())
    return True

def size():
    return len(words)

def unload():
    return True
