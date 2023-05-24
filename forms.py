from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length, ValidationError

class UserSignUpForm(FlaskForm):
    first = StringField("First Name", validators=[DataRequired()])
    last = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[
        DataRequired(),
        Regexp(r'^\w+$', message="Username must contain only letters, digits, or underscores"),
        Regexp(r'^(?!.*\s)', message="Username cannot contain spaces")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=7, message="Password must be at least 7 characters long")
    ])
    submit_button = SubmitField()

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken. Please choose a different username.')
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already registered. Please choose a different email.')

class UserSignInForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit_button = SubmitField()