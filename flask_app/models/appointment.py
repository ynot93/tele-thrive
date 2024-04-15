from flask_app import db
from sqlalchemy.sql import func


class Appointment(db.Model):
    """
    Appointment model class to represent appointments in the database.

    Attributes:
        id (int): Unique identifier for the appointment.
        date (datetime.date): Date of the appointment.
        time (datetime.time): Time of the appointment.
        description (str): Description of the appointment.
        user_id (int): Foreign key referencing the User table for the client associated with the appointment.
        therapist_id (int): Foreign key referencing the Therapist table for the therapist associated with the appointment.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Appointment object.

        Returns:
            str: A string representation of the Appointment object.
        """
        return f"Appointment('{self.appointment_name}', '{self.appointment_date}')"
