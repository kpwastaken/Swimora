from app import app
from models import SwimStandard

with app.app_context():

    standards = SwimStandard.query.all()

    for s in standards:
        print(s.age, s.gender, s.pool, s.event)
