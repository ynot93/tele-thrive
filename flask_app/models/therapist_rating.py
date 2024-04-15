from flask_app import db

class TherapistRating(db.Model):
    """
    TherapistRating class represents the ratings given by users to therapists.

    Attributes:
        id (int): The primary key of the TherapistRating.
        therapist_id (int): The foreign key referencing the therapist being rated.
        specialization (str): The specialization of the therapist.
        rating (int): The rating given to the therapist.
        description (str): Additional description or feedback for the rating.
        user_id (int): The foreign key referencing the user who gave the rating.
    """
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        """
        Returns a string representation of the TherapistRating object.

        Returns:
            str: A string containing the therapist's ID and rating.
        """
        return f"TherapistRating(Therapist ID: {self.therapist_id}, Rating: {self.rating})"
