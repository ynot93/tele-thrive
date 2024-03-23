from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm, TherapistRegistrationForm, TherapistLoginForm
from . import app

from models.appointment import Appointment
from models.therapist import Therapist
from models.user import User


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
        flash(f'Account created for {form.username.data}!', 'sucess')
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'tony@blog.com' and form.password.data == 'password':
            flash(f'You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Check username and Password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/register/therapist", methods=['GET', 'POST'])
def register_therapist():
    form = TherapistRegistrationForm()
    if form.validate_on_submit():
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
