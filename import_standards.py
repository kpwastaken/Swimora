import tabula
import pandas as pd

from app import app
from models import db, SwimStandard


PDF_FILE = "standards.pdf"


levels = [
    "B",
    "BB",
    "A",
    "AA",
    "AAA",
    "AAAA"
]


def clean_time(value):
    if pd.isna(value):
        return None

    value = str(value).replace("*", "").strip()

    if value == "":
        return None

    return value



def import_data():

    tables = tabula.read_pdf(
        PDF_FILE,
        pages="all",
        multiple_tables=True
    )

    count = 0

    current_age = None
    current_gender = None
    current_pool = None


    for table in tables:

        table = table.fillna("")


        for _, row in table.iterrows():

            row_text = " ".join(
                str(x) for x in row.values
            )


            # Detect age and gender
            if "Girls" in row_text or "Boys" in row_text:
                if "Girls" in row_text:
                    current_gender = "Female"

                if "Boys" in row_text:
                    current_gender = "Male"


                numbers = [
                    int(x)
                    for x in row_text.split()
                    if x.isdigit()
                ]

                if numbers:
                    current_age = numbers[0]


            # Detect event
            event = None

            for value in row.values:

                value = str(value)

                if "FR" in value or "BK" in value or "BR" in value or "FL" in value or "IM" in value:

                    event = value.strip()

                    break


            if not event:
                continue


            # Detect pool
            if "SCY" in event:
                current_pool = "SCY"

            elif "SCM" in event:
                current_pool = "SCM"

            elif "LCM" in event:
                current_pool = "LCM"


            times = []


            for value in row.values:

                cleaned = clean_time(value)

                if cleaned:
                    times.append(cleaned)



            # Remove event name
            times = [
                t for t in times
                if ":" in t or "." in t
            ]


            if len(times) < 6:
                continue



            for level, time in zip(levels, times[:6]):

                standard = SwimStandard(
                    region="USA Swimming",
                    pool=current_pool,
                    gender=current_gender,
                    age=current_age,
                    event=event,
                    level=level,
                    time=time
                )

                db.session.add(standard)

                count += 1



    db.session.commit()

    print(
        f"Imported {count} swimming standards!"
    )



if __name__ == "__main__":

    with app.app_context():

        import_data()