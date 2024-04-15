import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = Flask(__name__)
# Set secret key for the app to prevent CSRF attacks
app.secret_key = os.environ.get('SECRET_KEY')
# Set database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# Disable modification tracking as it is unnecessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAlchemy database instance
db = SQLAlchemy(app)
# Push app context to run the app instance
app.app_context().push() # runs the app instance
# Create Bcrypt instance for password hashing
bcrypt = Bcrypt(app)
# Create LoginManager instance for user authentication
login_manager = LoginManager(app)
# Set the login view for the LoginManager
login_manager.login_view = 'login'
# Set the login message category for LoginManager
login_manager.login_message_category = 'info'

from . import routes
from flask_app.models.user import User
from flask_app.models.therapist import Therapist


@login_manager.user_loader
def load_user(uuid):
    """
    Load a user from the database based on the provided UUID.
    Args:
        uuid (str): The UUID of the user to load.
    Returns:
        User or None: The user object if found, None otherwise.
    """
    # Dispatch user loading based on user type
    user_types = [User, Therapist]
    for user_type in user_types:
        user = user_type.query.get(int(uuid))
        if user:
            return user
    return None
