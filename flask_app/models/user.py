from flask_app import db
from sqlalchemy.sql import func
from flask_app import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # role = db.Column(db.String(20), nullable=False)
    
    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"