import unittest
from flask_app import create_app, db
from flask_app.models.therapist import Therapist

class TestTherapistModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_therapist(self):
        therapist = Therapist(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@example.com',
            password='password',
            license_number=123456
                                                                        )
        db.session.add(therapist)
        db.session.commit()

        retrieved_therapist = Therapist.query.filter_by(username='johndoe').first()
        self.assertIsNotNone(retrieved_therapist)
        self.assertEqual(retrieved_therapist.first_name, 'John')
        self.assertEqual(retrieved_therapist.last_name, 'Doe')
        self.assertEqual(retrieved_therapist.email, 'johndoe@example.com')
        self.assertEqual(retrieved_therapist.license_number, 123456)


