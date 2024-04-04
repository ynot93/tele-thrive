from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_security import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_app.models.user import User
from flask_app.models.therapist import Therapist


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists!')


class TherapistRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    license_number = StringField(
        'License Number',
        validators=[DataRequired(), Length(min=6, max=12)]
    )
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        email = Therapist.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists!')
        
    def validate_username(self, username):
        therapist = Therapist.query.filter_by(username=username.data).first()
        if therapist:
            raise ValidationError('This username already exists!')
        
    def validate_license_number(self, license_number):
        license_number = Therapist.query.filter_by(license_number=license_number.data).first()
        if license_number:
            raise ValidationError('This license_number is already in use!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# class TherapistLoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    prof_pic = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already exists!')


class UpdateTherapistProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    prof_pic = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            client = User.query.filter_by(username=username.data).first()
            therapist = Therapist.query.filter_by(username=username.data).first()
            if client or therapist:
                raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email_client = User.query.filter_by(email=email.data).first()
            email_therapist = Therapist.query.filter_by(email=email.data).first()
            if email_client or email_therapist:
                raise ValidationError('This email already exists!')