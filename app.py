from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'd6dafdfc696f40436c0a37834456059f'

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


if __name__ == "__main__":
    app.run(debug=True)
