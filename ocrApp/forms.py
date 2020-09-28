from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    first_name = StringField('first name', validators=[InputRequired(), Length(min=1, max=20)])
    last_name = StringField('last name', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
