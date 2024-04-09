from flask_app import db
# from flask_app.models.user import Base
from flask_login import UserMixin
from flask_app.models.user import random_integer


class Therapist(db.Model, UserMixin):
    id = db.Column(db.String,  default=random_integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    license_number = db.Column(db.Integer, nullable=False, unique=True)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    ratings = db.relationship('TherapistRating', backref='therapist', lazy=True)

    def __repr__(self):
        return f"Therapist('{self.username}', '{self.email}', '{self.license_number}')"