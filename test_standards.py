from app import app
from models import SwimStandard

with app.app_context():

    standards = SwimStandard.query.all()

    print("Total standards:", len(standards))

    for s in standards:
        print(
            s.gender,
            s.age,
            s.event,
            s.level,
            s.time
        )