import unittest
from flask_app import db
from flask_app.models.user import User

class TestUserModel(unittest.TestCase):

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')

    def test_unique_constraints(self):
        with self.assertRaises(IntegrityError):
            user1 = User(username='testuser', email='test@example.com', password='password')
            user2 = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    def test_nullable_constraints(self):
        # Attempt to create a user with missing required fields
        with self.assertRaises(ValueError):
            # Missing username
            user1 = User(email='test@example.com', password='password')
            db.session.add(user1)
            db.session.commit()

        with self.assertRaises(ValueError):
            # Missing email
            user2 = User(username='testuser', password='password')
            db.session.add(user2)
            db.session.commit()

        with self.assertRaises(ValueError):
            # Missing password
            user3 = User(username='testuser', email='test@example.com')
            db.session.add(user3)
            db.session.commit()

        self.assertEqual(user.image_profile, 'default.jpg')
  
