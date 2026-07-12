from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    weekly_goal = db.Column(db.Integer, default=20000)
    goal_name = db.Column(
        db.String(100),
        default="Weekly Distance Goal"
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    team = db.Column(db.String(100))
    stroke = db.Column(db.String(50))
    event = db.Column(db.String(50))

    avatar_emoji = db.Column(

        db.String(10),

        default="🏊"

    )

    avatar_color = db.Column(

        db.String(20),

        default="#0d6efd"

    )


    workouts = db.relationship(
        "Workout",
        backref="swimmer",
        lazy=True
    )


    pbs = db.relationship(
        "PersonalBest",
        backref="swimmer",
        lazy=True
    )



class Workout(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(20))

    distance = db.Column(db.Integer)

    workout_type = db.Column(db.String(50))

    stroke = db.Column(db.String(50))

    notes = db.Column(db.Text)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )



class PersonalBest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    event = db.Column(db.String(50))

    time = db.Column(db.String(20))

    date = db.Column(db.String(20))

    meet = db.Column(db.String(100))

    notes = db.Column(db.Text)



    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

