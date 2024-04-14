import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push() # runs the app instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from . import routes
from flask_app.models.user import User
from flask_app.models.therapist import Therapist


@login_manager.user_loader
def load_user(uuid):
    # Dispatch user loading based on user type
    user_types = [User, Therapist]
    for user_type in user_types:
        user = user_type.query.get(int(uuid))
        if user:
            return user
    return None