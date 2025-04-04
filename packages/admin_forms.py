from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired,Email


class AdminLogin(FlaskForm):
    username = EmailField('Username', validators=[DataRequired('Username is required')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Login')

    class Meta:
        csrf = True
csrf_time_limit = 360




class AdminRegister(FlaskForm):
    username = StringField('User Name', validators=[DataRequired('Please enter your username')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 360


      

