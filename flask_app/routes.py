import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, TherapistRegistrationForm, UpdateProfileForm, UpdateTherapistProfileForm
from . import app, db, bcrypt
from flask_app.analysis import get_custom_response
from flask_app.models.appointment import Appointment
from flask_app.models.therapist import Therapist
from flask_app.models.user import User
from flask import session
# from .id_generator import generate_unique_user_id, generate_unique_therapist_id
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    print(current_user)
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/for-therapist")
def for_therapist():
    return render_template("for_therapist.html", title='For Therapist')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pwd)
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
        therapist = Therapist.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'You have successfully logged in as a client!', 'success')
                next_redirect = request.args.get('next')
                return redirect(next_redirect) if next_redirect else redirect(url_for('dashboard'))
            else:
                flash(f'Incorrect email or password. Please try again.', 'danger')
        elif therapist:
            if bcrypt.check_password_hash(therapist.password, form.password.data):
                login_user(therapist, remember=form.remember.data)
                flash('You have successfully logged in as a therapist!', 'success')
                next_redirect = request.args.get('next')
                return redirect(next_redirect) if next_redirect else redirect(url_for('dashboard'))
            else:
                flash(f'Incorrect email or password. Please try again.', 'danger')
        else:
            flash(f'User does not exist. Please sign up.', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/register/therapist", methods=['GET', 'POST'])
def register_therapist():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = TherapistRegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        therapist = Therapist(first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              username=form.username.data,
                              email=form.email.data,
                              password=hashed_pwd,
                              license_number=form.license_number.data)
        db.session.add(therapist)
        db.session.commit()
        flash(f'Therapist account created for {form.first_name.data} {form.last_name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template("register_therapist.html", title='Therapist Registration', form=form)


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

@app.route("/logout")
def logout():
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
    

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    print(current_user)
    if isinstance(current_user, User):
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
        return render_template('user_dashboard.html', title='User Profile',
                            profile_pic=profile_pic, form=form)
    elif isinstance(current_user, Therapist):
        form = UpdateTherapistProfileForm()
        if form.validate_on_submit():
            if form.prof_pic.data:
                old_picture = current_user.image_profile
                if old_picture != 'default.jpg':
                    os.remove(os.path.join(app.root_path,
                                        'static/images/profile_pictures',
                                        old_picture))
                saved_picture = save_pic(form.prof_pic.data)
                current_user.image_profile = saved_picture
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('therapist_profile'))
        elif request.method == 'GET':
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_pic = url_for('static', filename='images/profile_pictures/' + current_user.image_profile)
        return render_template('therapist_dashboard.html', title='User Profile',
                            profile_pic=profile_pic, form=form)
    else:
        return redirect(url_for('home'))
    

@app.route("/health-analysis", methods=['GET', 'POST'])
def health_analysis():    
    if request.method == 'POST':
        scores = []
        for i in range(1, 13):
            response = request.form.get(f"optradio{i}")
            if response is None:
                flash("Please answer all questions to get accurate results.", "danger")
                return redirect(url_for('health_analysis'))
            scores.append(int(response))
        
        personality_level = sum(scores[:3]) / 3
        anxiety_level = sum(scores[5:8]) / 3
        depression_level = sum(scores[9:]) / 3
        
        custom_response = get_custom_response(personality_level,
                                              anxiety_level,
                                              depression_level)
        
        session['custom_response'] = custom_response
    
        return redirect(url_for('display_results'))

    return render_template('health_analysis.html',
                           title='Health Analysis')


@app.route("/display-results")
def display_results():
    response = session.get('custom_response')
    
    return render_template('results.html', response=response)