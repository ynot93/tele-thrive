import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, TherapistRegistrationForm, UpdateProfileForm, UpdateTherapistProfileForm, AppointmentForm
from . import app, db, bcrypt
from flask_app.analysis import get_custom_response
from flask_app.models.appointment import Appointment
from flask_app.models.therapist import Therapist
from flask_app.models.user import User
from flask_app.models.therapist_rating import TherapistRating
from flask_app.models.post import Post
from flask import session
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify
import uuid


@app.route("/")
@app.route("/home")
def home():
    """
    Render the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    active_nav = 'home'
    return render_template("home.html", active_nav=active_nav)


@app.route("/about")
def about():
    """
    Render the about page.

    Returns:
        str: Rendered HTML template for the about page.
    """
    active_nav = 'about'
    return render_template("about.html", title='About', active_nav=active_nav)

@app.route("/for-therapist")
def for_therapist():
    """
    Render the for therapist page.

    Returns:
    str: Rendered HTML template for the for therapist page.
    """
    active_nav = 'for_therapist'
    return render_template("for_therapist.html", title='For Therapist', active_nav=active_nav)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Render the registration page and handle user registration.

    Returns:
        str: Rendered HTML template for the registration page.
    """
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
    """
    Render the login page and handle user login.

    Returns:
        str: Rendered HTML template for the login page.
    """
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
    """
    Render the therapist registration page and handle therapist registration.

    Returns:
        str: Rendered HTML template for the therapist registration page.
    """
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


@app.route("/dashboard/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    """
    Render the appointments page and handle appointment creation.

    Returns:
        str: Rendered HTML template for the appointments page.
    """
    active_nav = 'appointments'
    active_nav_db = 'dashboard'
    
    user_type = "user" if isinstance(current_user, User) else "therapist"
    
    appointments = Appointment.query.filter(Appointment.user_id == current_user.id).all()
    therapist_appointments = Appointment.query.filter(Appointment.therapist_id == current_user.id).all()
    
    form = AppointmentForm()
    
    form.therapist.choices = [(therapist.id, f'{therapist.first_name} {therapist.last_name}') for therapist in Therapist.query.all()]
    form.user.choices = [(user.id, f'{user.username}') for user in User.query.all()]
    
    if not form.therapist.choices:
            flash('No Therapists are available yet', 'danger')
        
    if user_type == "user" and form.validate_on_submit():
        new_appointment = Appointment(
            user_id=current_user.id,
            therapist_id=form.therapist.data,
            date=form.date.data,
            time=form.time.data,
            description=form.description.data,
            meeting_url=str(uuid.uuid4())
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment created successfully!', 'success')
        return redirect(url_for('appointments'))
            
    elif user_type == 'therapist' and form.validate_on_submit():
        new_appointment = Appointment(
            therapist_id=current_user.id,
            user_id=form.user.data,
            date=form.date.data,
            time=form.time.data,
            description=form.description.data,
            meeting_url=str(uuid.uuid4())
        )
            
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment created successfully!', 'success')
        return redirect(url_for('appointments'))
    return render_template("appointments.html",
                           form=form,
                           active_nav=active_nav,
                           active_nav_db=active_nav_db,
                           appointments=appointments,
                           therapist_appointments=therapist_appointments,
                           user_type=user_type)


@app.route("/dashboard/appointments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_appointment(id):
    active_nav = 'appointments'
    active_nav_db = 'dashboard'
    
    user_type = "user" if isinstance(current_user, User) else "therapist"
    
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)
    
    form.therapist.choices = [(therapist.id, f'{therapist.first_name} {therapist.last_name}') for therapist in Therapist.query.all()]
    form.user.choices = [(user.id, f'{user.username}') for user in User.query.all()]
    
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointments'))
    elif request.method == 'GET':
        form.date.data = appointment.date
        form.time.data = appointment.time
        form.description.data = appointment.description
        if current_user == 'user':
            form.therapist.data = appointment.therapist_id
        elif current_user == 'therapist':
            form.user.data = appointment.user_id
    return render_template('edit_appointment.html',
                           form=form,
                           active_nav=active_nav,
                           active_nav_db=active_nav_db,
                           appointment=appointment,
                           user_type=user_type)


@app.route("/dashboard/appointments/delete/<int:id>", methods=["POST"])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointments'))


@app.route('/therapists', methods=['GET'])
def get_therapists():
    """
    Get a list of therapists.

    Returns:
        str: JSON representation of therapist data.
    """
    therapists = Therapist.query.filter_by(specialization='filter_value').all()
    therapist_data = [therapist.serialize() for therapist in therapists]
    return jsonify(therapist_data)


@app.route('/therapists/<therapist_id>/rate', methods=['POST'])
def rate_therapist(therapist_id):
    """
    Rate a therapist.

    Args:
        therapist_id (str): The ID of the therapist being rated.

    Returns:
        str: JSON response confirming the rating submission.
    """
    therapist = Therapist.query.get(therapist_id)
    rating = request.json.get('rating')
    therapist_rating = TherapistRating(therapist_id=therapist_id, rating=rating)
    db.session.add(therapist_rating)
    db.session.commit()
    return jsonify({'message': 'Rating submitted successfully'})


# Render therapists.html template
@app.route('/dashboard/therapists', methods=['GET'])
def view_therapists():
    """
    Render the view therapists page.

    Returns:
        str: Rendered HTML template for the view therapists page.
    """
    active_nav = 'therapists'
    active_nav_db = 'dashboard'
    therapists = Therapist.query.all()
    return render_template('therapists.html', therapists=therapists, active_nav=active_nav, active_nav_db=active_nav_db)


# Render rate_therapist.html template
@app.route('/therapists/<therapist_id>/rate', methods=['GET'])
def view_rate_therapist(therapist_id):
    """
    Render the rate therapist page.

    Args:
        therapist_id (str): The ID of the therapist being rated.

    Returns:
        str: Rendered HTML template for the rate therapist page.
    """
    therapist = Therapist.query.get(therapist_id)
    return render_template('rate_therapist.html', therapist=therapist)

 
@app.route("/logout")
def logout():
    """
    Log out the user.

    Returns:
        str: Redirects to the home page after logging out.
    """
    logout_user()
    return redirect(url_for('home'))


def save_pic(picture):
    """
    Save a profile picture.

    Args:
        picture (file): The image file to be saved.

    Returns:
        str: The filename of the saved picture.
    """
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
@app.route("/dashboard/profile", methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the dashboard page.

    Returns:
        str: Rendered HTML template for the dashboard page.
    """
    print(current_user)
    active_nav = 'profile'
    active_nav_db = 'dashboard'
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
            return redirect(url_for('dashboard'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_pic = url_for('static', filename='images/profile_pictures/' + current_user.image_profile)
        return render_template('user_dashboard.html', title='User Profile',
                            profile_pic=profile_pic, form=form, active_nav=active_nav, active_nav_db=active_nav_db)
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
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('dashboard'))
        elif request.method == 'GET':
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_pic = url_for('static', filename='images/profile_pictures/' + current_user.image_profile)
        return render_template('therapist_dashboard.html', title='User Profile',
                            profile_pic=profile_pic, form=form, active_nav=active_nav, active_nav_db=active_nav_db)
    else:
        return redirect(url_for('home'))


@app.route("/health-analysis", methods=['GET', 'POST'])
def health_analysis():
    """
    Perform health analysis.

    Returns:
        str: Rendered HTML template for the health analysis page.
    """
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
    """
    Display health analysis results.

    Returns:
        str: Rendered HTML template for displaying health analysis results.
    """
    response = session.get('custom_response')
    
    return render_template('results.html', response=response)

  
@app.route("/meeting")
@login_required
def existing_meeting():
    """
    Render the meeting page.
    """
    return render_template('meeting.html', username=current_user.username)


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    """
    Handle joining a meeting.
    """
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
    """
    Render the therapist meeting page.
    """

    if isinstance(current_user, Therapist):
        return render_template('meeting.html', username=current_user.username)


@app.route("/therapist/join", methods=["GET", "POST"])
@login_required
def therapist_join():
    """
    Handle therapist joining a meeting.
    """
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/therapist/meeting?roomID={room_id}")
    return render_template('join.html')


@app.route("/meeting/<meeting_id>")
@login_required
def meeting(meeting_id):
    """
    Render the meeting page.
    """
    appointment = Appointment.query.filter_by(meeting_url=meeting_id).first_or_404()
    return render_template('meeting.html', appointment=appointment, username=current_user.username)


@app.route('/posts', methods=['GET'])
@login_required
def posts():
    # Retrieve all posts from the database
    posts = Post.query.all()
    # Serialize the posts into JSON format
    serialized_posts = [{'id': post.id, 'content': post.content, 'author': post.author.username} for post in posts]
    return render_template('posts.html')


@app.route('/posts', methods=['POST'])
@login_required
def create_post():
    """
    Retrieve posts from the database.
    """
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    # Create a new post
    new_post = Post(content=content, author=current_user)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'id': new_post.id}), 201
