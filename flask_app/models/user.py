from flask_app import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from random import randint 

def random_integer():
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)
    
    return rand


class User(db.Model, UserMixin):
    id = db.Column(db.String,  default=random_integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')

    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.username}', '{self.email}')"
