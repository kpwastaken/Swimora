import csv

from app import app
from models import db, SwimStandard


CSV_FILE = "standards.csv"


def import_data():

    count = 0

    with open(CSV_FILE, newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            gender = row["Gender"]

            if gender == "Boys":
                gender = "Male"
            elif gender == "Girls":
                gender = "Female"

            for level in ["B", "BB", "A", "AA", "AAA", "AAAA"]:

                standard = SwimStandard(
                    region="USA Swimming",
                    pool=row["Course"],
                    gender=gender,
                    age=int(row["Age"]),
                    event=row["Event"],
                    level=level,
                    time=row[level]
                )

                db.session.add(standard)
                count += 1

    db.session.commit()

    print(f"Imported {count} standards!")

if __name__ == "__main__":

    with app.app_context():
        import_data()