"""
Application forms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
                    TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
                               ValidationError
from flaskblog.models import User
"""
Imports:
    flask wt forms:
        form fields
    flask_wtf.file
        filefield, FileAllowed used in update account form
    flask_login:
        current_user used in updateaccount form
    wt.forms: fields used in forms
    wt forms: validators used in var declaratoins
    wt forms: validationerror used in custom field validation function
    user model: used in customr field validation function
"""


class RegistrationForm(FlaskForm):
    """
    Registration Form
    """
    # Create the html field and label, required and between 2-20 chars
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
        # todo: add minimum length
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validation if username is unique"""
        user = User.query.filter_by(username=username.data).first()
        # raise an error and send message to form
        if user:
            raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self, email):
        """Validation if email is unique"""
        user = User.query.filter_by(email=email.data).first()
        # raise an error and send message to form
        if user:
            raise ValidationError('Email already exists. Please choose another.')


    def validate_field(self, field):
        """Validation"""
        if True:
            raise ValueError('msg')


class LoginForm(FlaskForm):
    """
    Login form
    """# username = StringField('Username',
    #     validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
        # todo: add minimum length
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Update User Account Form
    """
    # Create the html field and label, required and between 2-20 chars
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    # profile pic update
    picture = FileField('Update profile picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    # todo when click on image
    submit = SubmitField('Update account')

    def validate_username(self, username):
        """Validation if username is unique"""
        # only validate if username is changed
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # raise an error and send message to form
            if user:
                raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self, email):
        """Validation if email is unique"""
        # only validate if email is changed
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # raise an error and send message to form
            if user:
                raise ValidationError('Email already exists. Please choose another.')


class PostForm(FlaskForm):
    """Show posts"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post it')


class RequestResetForm(FlaskForm):
    """Reset pw page to submit reset request"""
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        """Validation if email does not exist"""
        # get the user
        user = User.query.filter_by(email=email.data).first()
        # If email has no account
        if user is None:
            raise ValidationError('No account with email. register first!')


class ResetPasswordForm(FlaskForm):
    """
    Rest password form
    """
    password = PasswordField('Password',
        validators=[DataRequired()])
        # todo: add minimum length
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
