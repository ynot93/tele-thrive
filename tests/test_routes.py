import unittest
from flask import url_for
from flask_app import app, db
from flask_app.models.therapist import Therapist
from flask_app.models.user import User
import sys
import os

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to TeleThrive', response.data)

    def test_about_route(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About TeleThrive', response.data)

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_therapist_route(self):
        response = self.app.get('/register/therapist')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Therapist Registration', response.data)

    def test_registration_form_validation(self):
        response = self.app.post('/register', data={'username': '', 'email': 'invalid_email', 'password': '123'}, follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)  # Expecting error message for empty username
        self.assertIn(b'Invalid email address.', response.data)   # Expecting error message for invalid email

    def test_empty_form_submission(self):
        response = self.app.post('/register', data={}, follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_login_session(self):
        with self.app:
            response = self.app.post('/login', data={'email': 'test@example.com', 'password': 'test123'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(session.get('user_id'))  # Expecting user ID in session after successful login

    def test_get_therapists_route(self):
        response = self.app.get('/therapists')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Therapists List', response.data)

    def test_rate_therapist_route(self):
        with self.app:
            self.app.post('/login', data=dict(
                email='therapist@example.com', password='password'
            ), follow_redirects=True)
            response = self.app.post('/therapists/1/rate', json={
                'rating': 5,
                'specialization': 'Anxiety'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Rating submitted successfully', response.data)

    def test_logout_route(self):
        with self.app:
            self.app.post('/login', data=dict(
                email='user@example.com', password='password'
            ), follow_redirects=True)
            response = self.app.get('/logout')
            self.assertEqual(response.status_code, 302)

    def test_dashboard_route_as_user(self):
        with self.app:
            self.app.post('/login', data=dict(
                email='user@example.com', password='password'
            ), follow_redirects=True)
            response = self.app.get('/dashboard')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'login', response.data)

    def test_dashboard_route_as_therapist(self):
        with self.app:
            self.app.post('/login', data=dict(
                email='therapist@example.com', password='password'
            ), follow_redirects=True)
            response = self.app.get('/dashboard')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'login', response.data)

    def test_health_analysis_route_get(self):
        with self.app:
            response = self.app.get('/health-analysis')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Health Analysis', response.data)

    def test_display_results_route(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['custom_response'] = {'result': 'Some result'}
                response = self.app.get('/display-results')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Some result', response.data)

    def test_meeting_route(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a user is logged in
            response = self.app.get('/meeting')
            self.assertEqual(response.status_code, 302)

    def test_join_route_get(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a user is logged in
            response = self.app.get('/join')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'login', response.data)

    def test_join_route_post_as_user(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a user is logged in
            data = {'roomID': '123'}
            response = self.app.post('/join', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_join_route_post_as_therapist(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a therapist is logged in
            data = {'roomID': '123'}
            response = self.app.post('/join', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_therapist_meeting_route(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a therapist is logged in
            response = self.app.get('/therapist/meeting')
            self.assertEqual(response.status_code, 302)

    def test_therapist_join_route_post(self):
        with self.app:
            with self.app.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming a therapist is logged in
            data = {'roomID': '123'}
            response = self.app.post('/therapist/join', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_route(self):
        response = self.app.get('/invalid-route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Not Found', response.data)

    def test_authenticated_route_redirect(self):
        response = self.app.get('/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Expecting redirect status code
        self.assertIn(b'login', response.location.lower())
