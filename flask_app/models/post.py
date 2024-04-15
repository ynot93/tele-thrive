from flask_app import db
from sqlalchemy.sql import func


class Post(db.Model):
    """
    Post model class to represent posts in the database.

    Attributes:
        id (int): Unique identifier for the post.
        content (str): Content of the post.
        author_id (int): Foreign key referencing the User table for the author of the post.
        created_at (datetime.datetime): Timestamp indicating when the post was created.
        author (relationship): Relationship attribute representing the author of the post.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False,)

    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        """
        Return a string representation of the Post object.

        Returns:
            str: A string representation of the Post object.
        """
        return f"Post('{self.content}', '{self.created_at}')"
