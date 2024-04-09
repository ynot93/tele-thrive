import unittest
from flask_app import db
from datetime import datetime
from flask_app.models.appointment import Appointment


class TestAppointmentModel(unittest.TestCase):

    def test_create_appointment(self):
        appointment = Appointment(
                appointment_name='Therapy Session',
                status='Scheduled',
                user_id=1,
                therapist_id=1
                                                                        )
        db.session.add(appointment)
        db.session.commit()
        self.assertIsNotNone(appointment.id)

    def test_default_value(self):
        appointment = Appointment(
                appointment_name='Test Appointment',
                status='Scheduled',
                user_id=1,
                therapist_id=1
        )
        db.session.add(appointment)
        db.session.commit()
        self.assertIsNotNone(appointment.appointment_date)
        self.assertIsInstance(appointment.appointment_date, datetime)

