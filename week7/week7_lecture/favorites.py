import csv
from cs50 import SQL

db = SQL("sqlite:///favorites.db")

fav = input("Favorite: ")

rows = db.execute("SELECT COUNT(*) AS n FROM favorites WHERE problem = ?", fav)
row = rows[0]

print(row["n"])




'''
    with open("favorites.csv", "r") as file:
        reader = csv.DictReader(file)
        counts = {}

        for row in reader:
            fav = row["language"]
            if fav in counts:
                counts[fav] += 1
            else:
                counts[fav] = 1

    for item in sorted(counts, key=counts.get, reverse=True):
        print(f"{item}: {counts[item]}")'''


