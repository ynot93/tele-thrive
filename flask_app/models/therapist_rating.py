from flask_app import db

class TherapistRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"TherapistRating(Therapist ID: {self.therapist_id}, Rating: {self.rating})"
