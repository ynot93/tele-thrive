from flask_app import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from random import randint 

def random_integer():
    """
    Generate a random integer between 100 and 1000000000.
    """
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)
    
    return rand


class User(db.Model, UserMixin):
    """
    User class represents the users of the application.

    Attributes:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user was created.
        image_profile (str): The filename of the user's profile image.
        appointments (relationship): The appointments associated with the user.
    """
    id = db.Column(db.String,  default=random_integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')

    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string containing the username and email of the user.
        """
        return f"Client('{self.username}', '{self.email}')"
