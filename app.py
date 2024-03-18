from flask import Flask, render_template
from dotenv import load_dotenv
from forms import RegistrationForm
from flask_wtf import FlaskForm


load_dotenv()
app = Flask(__name__)

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title='Register', form=form)


if __name__ == "__main__":
    app.run(debug=True)
