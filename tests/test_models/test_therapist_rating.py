import unittest
from flask_app import db
from flask_app.models.therapist_rating import TherapistRating


class TestTherapistRatingModel(unittest.TestCase):

    def test_create_therapist_rating(self):
        therapist_rating = TherapistRating(
                therapist_id=1,
                specialization='Specialization',
                rating=4,
                description='Good therapist',
                user_id=1
        )
        db.session.add(therapist_rating)
        db.session.commit()
        self.assertIsNotNone(therapist_rating.id)
    
    def test_rating_range(self):
        # Test valid rating
        therapist_rating = TherapistRating(
                therapist_id=1,
                specialization='Specialization',
                rating=5,  # Valid rating
                user_id=1
        )
        db.session.add(therapist_rating)
        db.session.commit()
        self.assertIsNotNone(therapist_rating.id)

        # Test invalid rating (outside range)
        therapist_rating_invalid = TherapistRating(
                therapist_id=1,
                specialization='Specialization',
                rating=6,  # Invalid rating
                user_id=1
        )
        db.session.add(therapist_rating_invalid)
        with self.assertRaises(IntegrityError):
            db.session.commit() 
