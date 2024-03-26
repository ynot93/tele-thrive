from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm, TherapistRegistrationForm, TherapistLoginForm
from . import app

from flask_app.models.appointment import Appointment
from flask_app.models.therapist import Therapist
from flask_app.models.user import User
from flask import session
from flask import jsonify, request
from .id_generator import generate_unique_user_id, generate_unique_therapist_id


users = [
    {
        'first_name': "Tony",
        'last_name': "Mputhia",
        'date_created': "26/02/2024",
        'appointment': "12/04/2024",
        'age': 28
    },
    {
        'first_name': "Millyanne",
        'last_name': "Adhiambo",
        'date_created': "28/02/2024",
        'appointment': "17/04/2024",
        'age': 25
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", users=users)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = generate_unique_user_id()
        session['user_id'] = user_id
        flash(f'Account created for {form.username.data}!', 'sucess')
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            flash(f'You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Check username and Password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/register/therapist", methods=['GET', 'POST'])
def register_therapist():
    form = TherapistRegistrationForm()
    if form.validate_on_submit():
        therapist_id = generate_unique_therapist_id()
        session['therapist_id'] = therapist_id
        flash(f'Therapist account created for {form.first_name.data} {form.last_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register_therapist.html", title='Therapist Registration', form=form)


@app.route("/login/therapist", methods=['GET', 'POST'])
def login_therapist():
    form = TherapistLoginForm()
    if form.validate_on_submit():
        therapist = Therapist.query.filter_by(email=form.email.data).first()
        if therapist and therapist.check_password(form.password.data):
            flash('You have successfully logged in as a therapist!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check email and password', 'danger')
    return render_template('login_therapist.html', title='Therapist Login', form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))


#@app.route("/appointments", methods=["GET"])
#def get_appointments():
    #user_id = request.headers.get("User-Id")
    #if not user_id:
    #    return jsonify({"error": "User-Id header missing"}), 400
    #appointments = Appointment.query.filter_by(user_id=user_id).all()
    #appointment_data = [{
    #    "id": appointment.id,
    #    "appointment_name": appointment.appointment_name,
    #    "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d %H:%M:%S"),
    #    "status": appointment.status
    #} for appointment in appointments]

    #return jsonify(appointment_data), 200
   # pass


#@app.route("/appointments", methods=["POST"])
#def create_appointment():
   # user_id = request.headers.get("User-Id")
   # if not user_id:
   #     return jsonify({"error": "User not authenticated"}), 401
   # data = request.json
   # appointment_name = data.get("appointment_name")
   # appointment_date = data.get("appointment_date")
   # therapist_id = data.get("therapist_id")
   # status = "Scheduled"
   # if not all([appointment_name, appointment_date, therapist_id]):
   #     return jsonify({"error": "Incomplete data provided"}), 400
   # appointment = Appointment(
   #         appointment_name=appointment_name,
   #         appointment_date=appointment_date,
   #         status=status,
   #         user_id=user_id,
   #         therapist_id=therapist_id
   # )

   # db.session.add(appointment)
   # db.session.commit()

   # response_data = {
   #     "id": appointment.id,
   #     "appointment_name": appointment.appointment_name,
   #     "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d %H:%M:%S"),
   #     "status": appointment.status
   # }
   # return jsonify({"message": "Appointment created successfully", "appointment": response_data}), 201
 #  pass


@app.route("/appointments", methods=["GET"])
def get_appointments():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your appointments.", "danger")
        return redirect(url_for("login"))
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return render_template("appointments.html", appointments=appointments)


@app.route("/appointments/new", methods=["GET"])
def create_appointment():
    return render_template("create_appointment.html")
