import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, TherapistRegistrationForm, TherapistLoginForm, UpdateProfileForm
from . import app, db, bcrypt

from flask_app.models.appointment import Appointment
from flask_app.models.therapist import Therapist
from flask_app.models.user import User
from flask_app.models.therapist_rating import TherapistRating
from flask import session
from .id_generator import generate_unique_user_id, generate_unique_therapist_id
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # user_id = generate_unique_user_id()
        # session['user_id'] = user_id
        # flash(f'Account created for {form.username.data}!', 'sucess')
        # return redirect(url_for('home'))
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and user.password == form.password.data:
        #     session['user_id'] = user.id
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have successfully logged in!', 'success')
            session['role'] = 'user'
            next_redirect = request.args.get('next')
            return redirect(next_redirect) if next_redirect else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Check email or password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/register/therapist", methods=['GET', 'POST'])
def register_therapist():
    form = TherapistRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        therapist = Therapist(first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              email=form.email.data,
                              password=hashed_password)
        db.session.add(therapist)
        db.session.commit()
        flash(f'Therapist account created for {form.first_name.data} {form.last_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register_therapist.html", title='Therapist Registration', form=form)


@app.route("/login/therapist", methods=['GET', 'POST'])
def login_therapist():
    form = TherapistLoginForm()
    if form.validate_on_submit():
        therapist = Therapist.query.filter_by(email=form.email.data).first()
        if therapist and bcrypt.check_password_hash(therapist.password, form.password.data):
            login_user(therapist, remember=form.remember.data)
            flash('You have successfully logged in as a therapist!', 'success')
            session['role'] = 'therapist'
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check email and password', 'danger')
    return render_template('login_therapist.html', title='Therapist Login', form=form)


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


@app.route('/therapists', methods=['GET'])
def get_therapists():
    therapists = Therapist.query.filter_by(specialization='filter_value').all()
    therapist_data = [therapist.serialize() for therapist in therapists]
    return jsonify(therapist_data)


@app.route('/therapists/<therapist_id>/rate', methods=['POST'])
def rate_therapist(therapist_id):
    therapist = Therapist.query.get(therapist_id)
    rating = request.json.get('rating')
    therapist_rating = TherapistRating(therapist_id=therapist_id, rating=rating)
    db.session.add(therapist_rating)
    db.session.commit()
    return jsonify({'message': 'Rating submitted successfully'})


# Render therapists.html template
@app.route('/therapists', methods=['GET'])
def view_therapists():
    therapists = Therapist.query.all()
    return render_template('therapists.html', therapists=therapists)


# Render rate_therapist.html template
@app.route('/therapists/<therapist_id>/rate', methods=['GET'])
def view_rate_therapist(therapist_id):
    therapist = Therapist.query.get(therapist_id)
    return render_template('rate_therapist.html', therapist=therapist)

 
@app.route("/logout")
def logout():
    # session.clear()
    # flash('You have been logged out!', 'success')
    # return redirect(url_for('home'))
    logout_user()
    return redirect(url_for('home'))


def save_pic(picture):
    hex_value = secrets.token_hex(8)
    file_name, ext = os.path.splitext(picture.filename)
    new_filename = hex_value + ext
    file_path = os.path.join(app.root_path, 'static/images/profile_pictures', new_filename)
    
    pixel_size = (125, 125)
    img = Image.open(picture)
    img.thumbnail(pixel_size)
    img.save(file_path)
    return new_filename
    

@app.route("/user-profile", methods=['GET', 'POST'])
@login_required(role="ANY")
def user_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.prof_pic.data:
            old_picture = current_user.image_profile
            if old_picture != 'default.jpg':
                os.remove(os.path.join(app.root_path,
                                       'static/images/profile_pictures',
                                       old_picture))
            saved_picture = save_pic(form.prof_pic.data)
            current_user.image_profile = saved_picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('user_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='images/profile_pictures/' + current_user.image_profile)
    return render_template('user_profile.html', title='User Profile',
                           profile_pic=profile_pic, form=form)

@app.route("/meeting")
@login_required
def meeting():
    return render_template('meeting.html', username=current_user.username)


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        if isinstance(current_user, Therapist):
            return redirect(f"/therapist/meeting?roomID={room_id}")
        else:
            return redirect(f"/meeting?roomID={room_id}")
    return render_template('join.html')


@app.route("/therapist/meeting")
@login_required
def therapist_meeting():
    if isinstance(current_user, Therapist):
        return render_template('meeting.html', username=current_user.username)


@app.route("/therapist/join", methods=["GET", "POST"])
@login_required
def therapist_join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/therapist/meeting?roomID={room_id}")
    return render_template('join.html')
