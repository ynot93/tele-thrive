import unittest
from flask_app.forms import RegistrationForm, TherapistRegistrationForm, UpdateTherapistProfileForm
from flask_app import create_app, db
from flask_app.models.user import User
from flask_app.models.therapist import Therapist

class TestTherapistForms(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_therapist_registration_form_validations(self):
        # Test validation of unique username
        form = TherapistRegistrationForm(
                username='existing_username',
                email='test@example.com',
                password='password',
                confirm_password='password',
                license_number='123456'
        )
        self.assertFalse(form.validate())
        self.assertIn('This username already exists!', form.username.errors)

    def test_update_therapist_profile_form_validations(self):
        # Test validation of unique username and email
        existing_therapist = Therapist(
                first_name='John',
                last_name='Doe',
                username='existing_username',
                email='existing@example.com',
                password='password',
                license_number='123456'
        )
        db.session.add(existing_therapist)
        db.session.commit()
        form = UpdateTherapistProfileForm(
                username='existing_username',
                email='existing@example.com'
        )
        self.assertFalse(form.validate())
        self.assertIn('This username already exists!', form.username.errors)
        self.assertIn('This email already exists!', form.email.errors)

class TestForms(unittest.TestCase):
    def test_login_form_validations(self):
        form = LoginForm(
                email='test@example.com',
                password='password'
        )
        self.assertTrue(form.validate())

    def test_update_profile_form_validations(self):
        form = UpdateProfileForm(
                username='existing_username',
                email='test@example.com'
        )
        self.assertFalse(form.validate())
        self.assertIn('This username already exists!', form.username.errors)

class TestRegistrationForm(unittest.TestCase):
    def test_registration_form_validations(self):
        form = RegistrationForm(
                username='existing_username',
                email='test@example.com',
                password='password',
                confirm_password='password'
        )
        self.assertFalse(form.validate())
        self.assertIn('This username already exists!', form.username.errors)
    
    def test_validate_username_duplicate(self):
        form = RegistrationForm(username='testuser')
        result = form.validate_username('testuser')
        self.assertFalse(result)  # Expecting False because username is duplicate

    def test_validate_email_duplicate(self):
        form = RegistrationForm(email='test@example.com')
        result = form.validate_email('test@example.com')
        self.assertFalse(result)  # Expecting False because email is duplicate

    def test_validate_username_unique(self):
        form = RegistrationForm(username='newuser')
        result = form.validate_username('newuser')
        self.assertTrue(result)  # Expecting True because username is unique

    def test_validate_email_unique(self):
        form = RegistrationForm(email='new@example.com')
        result = form.validate_email('new@example.com')
        self.assertTrue(result)  # Expecting True because email is unique
