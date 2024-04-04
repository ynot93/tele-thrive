from flask_app import db
from flask_login import UserMixin


class Therapist(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # active = db.Column(db.Boolean())
    # specialization = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.Integer, nullable=False, unique=True)
    # role = db.Column(db.String(80), default='Therapist')
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"Therapist('{self.username}', '{self.email}', '{self.license_number}')"