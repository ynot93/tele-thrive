from flask_app import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    # role = db.Column(db.String(20), default='User')

    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.username}', '{self.email}')"
