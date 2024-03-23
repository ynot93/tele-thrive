from flask_app import db


class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.Integer, nullable=False, unique=True)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"Therapist('{self.therapist_name}', '{self.email}')"