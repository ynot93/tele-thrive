from flask_app import db
from sqlalchemy.sql import func


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_name = db.Column(db.Text, nullable=False)
    appointment_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(db.String(20), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)

    def __repr__(self):
        return f"Appointment('{self.appointment_name}', '{self.appointment_date}')"
