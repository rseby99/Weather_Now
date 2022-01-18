from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField, BooleanField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,Length
from WeatherNow.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('An account is already created using this email.  Please use another one !')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UserSettingsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    country = StringField('Country', validators=[Length(max=2, message="Country should be in ISO 3166 format")])
    city = StringField('City')
    unit = SelectField('System of measurement', choices=[('metric', 'Metric'),('imperial','Imperial')])
    submit = SubmitField('Save')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('An account is already created using this email.  Please use another one !')


class GetWeatherForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired() ,Length(max=2, message="Country should be in ISO 3166 format")])
    get_current_weather = SubmitField('Get Current Weather')
    get_weather_7days = SubmitField('Get Weather Forecast for 7 days')
