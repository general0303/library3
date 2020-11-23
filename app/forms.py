from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddAuthorForm(FlaskForm):
    name = StringField('Name of author')
    title1 = StringField('Title of 1st book')
    title2 = StringField('Title of 2st book')
    title3 = StringField('Title of 3st book')
    title4 = StringField('Title of 4st book')
    title5 = StringField('Title of 5st book')
    submit = SubmitField('Add author')


class AddBookForm(FlaskForm):
    name = StringField('Title of book')
    submit = SubmitField('Add book')


class DeleteAuthorForm(FlaskForm):
    name = StringField('Name of author')
    submit = SubmitField('Delete author')


class DeleteBookForm(FlaskForm):
    name = StringField('Title of book')
    submit = SubmitField('Delete book')


class EditAuthorForm(FlaskForm):
    name = StringField('Name of author')
    new_name = StringField('New name of author')
    title = StringField('Title of book')
    submit = SubmitField('Edit author')


class EditBookForm(FlaskForm):
    name = StringField('Title of book')
    new_name = StringField('New title of book')
    submit = SubmitField('Edit book')


class SearchBooksByAuthorForm(FlaskForm):
    name = StringField('Name of author')
    submit = SubmitField('Search books')


class SearchBooksByTitleForm(FlaskForm):
    name = StringField('Tittle of book')
    submit = SubmitField('Search books')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')