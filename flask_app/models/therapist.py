from flask_app import db
from flask_login import UserMixin
from flask_app.models.user import random_integer


class Therapist(db.Model, UserMixin):
    """
    Therapist model class to represent therapists in the database.

    Attributes:
        id (str): Unique identifier for the therapist.
        first_name (str): First name of the therapist.
        last_name (str): Last name of the therapist.
        username (str): Username of the therapist.
        email (str): Email address of the therapist.
        image_profile (str): File name of the therapist's profile image.
        password (str): Password hash of the therapist.
        license_number (int): License number of the therapist.

    Relationships:
        appointments (relationship): One-to-many relationship with Appointment model.
        ratings (relationship): One-to-many relationship with TherapistRating model.
    """""
    
    id = db.Column(db.String,  default=random_integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    license_number = db.Column(db.Integer, nullable=False, unique=True)

    # Define relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    ratings = db.relationship('TherapistRating', backref='therapist', lazy=True)

    def __repr__(self):
        """
        Return a string representation of the Therapist object.

        Returns:
            str: A string representation of the Therapist object.
        """
        return f"Therapist('{self.username}', '{self.email}', '{self.license_number}')"
