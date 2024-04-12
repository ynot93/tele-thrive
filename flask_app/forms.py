from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_security import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, TimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_app.models.user import User
from flask_app.models.therapist import Therapist


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """
        Validates the uniqueness of username.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        """
        Validates the uniqueness of email.
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists!')


class TherapistRegistrationForm(FlaskForm):
    """
    Form for therapist registration.
    """
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
        """
        Validates the uniqueness of therapist's email.
        """
        email = Therapist.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists!')
        
    def validate_username(self, username):
        """
        Validates the uniqueness of therapist's username.
        """
        therapist = Therapist.query.filter_by(username=username.data).first()
        if therapist:
            raise ValidationError('This username already exists!')
        
    def validate_license_number(self, license_number):
        """
        Validates the uniqueness of therapist's license number.
        """
        license_number = Therapist.query.filter_by(license_number=license_number.data).first()
        if license_number:
            raise ValidationError('This license_number is already in use!')


class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateProfileForm(FlaskForm):
    """
    Form for updating user profile.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    prof_pic = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        """
        Validates the uniqueness of updated username.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        """
        Validates the uniqueness of updated email.
        """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already exists!')


class UpdateTherapistProfileForm(FlaskForm):
    """
    Form for updating therapist profile.
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    prof_pic = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        """
        Validates the uniqueness of updated username for therapist.
        """
        if username.data != current_user.username:
            client = User.query.filter_by(username=username.data).first()
            therapist = Therapist.query.filter_by(username=username.data).first()
            if client or therapist:
                raise ValidationError('This username already exists!')
    
    def validate_email(self, email):
        """
        Validates the uniqueness of updated email for therapist.
        """
        if email.data != current_user.email:
            email_client = User.query.filter_by(email=email.data).first()
            email_therapist = Therapist.query.filter_by(email=email.data).first()
            if email_client or email_therapist:
                raise ValidationError('This email already exists!')
    
    
class AppointmentForm(FlaskForm):
    """
    Form for creating appointments.
    """
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows": 5, "cols": 50})
    therapist = SelectField('Therapist', coerce=int, validators=[DataRequired()], render_kw={"rows": 5})
    user = SelectField('Client', coerce=int, validators=[DataRequired()], render_kw={"rows": 5})

    submit = SubmitField('Create Appointment')
    
    def validate_date(self, date):
        """
        Validates the appointment date.
        """
        if date.data < datetime.now().date():
            raise ValidationError('Date cannot be in the past.')

    def validate_time(self, time):
        """
        Validates the appointment time.
        """
        if self.date.data == datetime.now().date() and time.data <= datetime.now().time():
            raise ValidationError('Time cannot be in the past.')
