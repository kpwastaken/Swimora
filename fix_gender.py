from app import app
from models import db, SwimStandard

with app.app_context():
    SwimStandard.query.filter_by(gender="Boys").update({"gender": "Male"})
    SwimStandard.query.filter_by(gender="Girls").update({"gender": "Female"})
    db.session.commit()
    print("Done!")