from flask import Flask, render_template, request, redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Workout, PersonalBest


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()



@app.route("/")
def home():
    return redirect("/login")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=generate_password_hash(
                request.form["password"]
            )
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")


    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form["email"]
        ).first()


        if user and check_password_hash(
            user.password,
            request.form["password"]
        ):

            login_user(user)

            return redirect("/dashboard")


    return render_template("login.html")



@app.route("/dashboard")
@login_required
def dashboard():
    workouts = Workout.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Workout.id.desc()
    ).all()


    pbs = PersonalBest.query.filter_by(
        user_id=current_user.id
    ).all()


    total_distance = sum(
        workout.distance
        for workout in workouts
        if workout.distance
    )


    return render_template(
        "dashboard.html",
        user=current_user,
        workouts=workouts,
        total_distance=total_distance,
        workout_count=len(workouts),
        pb_count=len(pbs)
    )



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.age = request.form["age"]
        current_user.team = request.form["team"]
        current_user.stroke = request.form["stroke"]
        current_user.event = request.form["event"]

        db.session.commit()

        return redirect("/dashboard")


    return render_template(
        "profile.html",
        user=current_user
    )


@app.route("/generate_workout", methods=["GET", "POST"])
@login_required
def generate_workout():
    if request.method == "POST":

        stroke = request.form.get("stroke")
        goal = request.form.get("goal")
        distance = request.form.get("distance")
        time = request.form.get("time")
        level = request.form.get("level")

        if not stroke or not goal or not distance or not time or not level:
            return render_template(
                "generate_workout.html",
                error="Please fill in all fields before generating your workout."
            )

        distance = int(distance)
        time = int(time)


        if goal == "Speed":

            workout_sets = [
                f"400m warm up ({stroke})",
                "8 x 50m sprint",
                f"{max(4, distance // 100)} x 100m race pace",
                "200m cool down"
            ]


        elif goal == "Endurance":

            workout_sets = [
                f"600m warm up ({stroke})",
                f"{max(3, distance // 500)} x 500m steady pace",
                "8 x 50m technique drills",
                "300m cool down"
            ]


        elif goal == "Technique":

            workout_sets = [
                "400m easy swim",
                "8 x 50m technique drills",
                f"{max(4, distance // 100)} x 100m perfect technique",
                "200m cool down"
            ]


        else:

            workout_sets = [
                "500m warm up",
                f"{max(4, distance // 200)} x 200m race pace",
                "12 x 25m sprint",
                "300m cool down"
            ]


        return render_template(
            "generated_workout.html",
            stroke=stroke,
            goal=goal,
            distance=distance,
            time=time,
            level=level,
            workout_sets=workout_sets
        )


    return render_template(
        "generate_workout.html"
    )



@app.route("/save_generated_workout", methods=["POST"])
@login_required
def save_generated_workout():

    workout = Workout(
        date="AI Generated",
        distance=int(request.form["distance"]),
        workout_type=request.form["goal"],
        stroke=request.form["stroke"],
        notes="AI Generated Workout",
        user_id=current_user.id
    )


    db.session.add(workout)
    db.session.commit()


    return redirect("/workouts")
@app.route("/settings")
@login_required
def settings():

    return render_template("settings.html")



@app.route("/workouts")
@login_required
def workouts():

    user_workouts = Workout.query.filter_by(
        user_id=current_user.id
    ).all()


    return render_template(
        "workout.html",
        workouts=user_workouts
    )



@app.route("/add_workout", methods=["POST"])
@login_required
def add_workout():

    workout = Workout(
        date=request.form["date"],
        distance=request.form["distance"],
        workout_type=request.form["workout_type"],
        stroke=request.form["stroke"],
        notes=request.form["notes"],
        user_id=current_user.id
    )


    db.session.add(workout)
    db.session.commit()


    return redirect("/workouts")



@app.route("/edit_workout/<int:id>", methods=["GET", "POST"])
@login_required
def edit_workout(id):

    workout = Workout.query.get_or_404(id)


    if workout.user_id != current_user.id:
        return redirect("/workouts")


    if request.method == "POST":

        workout.date = request.form["date"]
        workout.distance = request.form["distance"]
        workout.workout_type = request.form["workout_type"]
        workout.stroke = request.form["stroke"]
        workout.notes = request.form["notes"]

        db.session.commit()

        return redirect("/workouts")


    return render_template(
        "edit_workout.html",
        workout=workout
    )



@app.route("/delete_workout/<int:id>")
@login_required
def delete_workout(id):

    workout = Workout.query.get_or_404(id)


    if workout.user_id == current_user.id:

        db.session.delete(workout)
        db.session.commit()


    return redirect("/workouts")



@app.route("/pbs")
@login_required
def pbs():

    user_pbs = PersonalBest.query.filter_by(
        user_id=current_user.id
    ).all()


    return render_template(
        "pbs.html",
        pbs=user_pbs
    )



@app.route("/add_pb", methods=["POST"])
@login_required
def add_pb():

    pb = PersonalBest(
        event=request.form["event"],
        time=request.form["time"],
        date=request.form["date"],
        meet=request.form["meet"],
        notes=request.form["notes"],
        user_id=current_user.id
    )


    db.session.add(pb)
    db.session.commit()


    return redirect("/pbs")



@app.route("/edit_pb/<int:id>", methods=["GET", "POST"])
@login_required
def edit_pb(id):

    pb = PersonalBest.query.get_or_404(id)


    if pb.user_id != current_user.id:
        return redirect("/pbs")


    if request.method == "POST":

        pb.event = request.form["event"]
        pb.time = request.form["time"]
        pb.date = request.form["date"]
        pb.meet = request.form["meet"]
        pb.notes = request.form["notes"]

        db.session.commit()

        return redirect("/pbs")


    return render_template(
        "edit_pb.html",
        pb=pb
    )



@app.route("/delete_pb/<int:id>")
@login_required
def delete_pb(id):

    pb = PersonalBest.query.get_or_404(id)


    if pb.user_id == current_user.id:

        db.session.delete(pb)
        db.session.commit()


    return redirect("/pbs")



@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")



if __name__ == "__main__":
    app.run(debug=True)