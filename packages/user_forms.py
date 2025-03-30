from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,SelectField
from wtforms import DateTimeLocalField,FileField,TelField,TimeField,DateField
from wtforms.validators import DataRequired,Email


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    pwd = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Login')

    class Meta:
        csrf = True
csrf_time_limit = 360

class ArtistForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired('Please enter you firstname')])
    lname = StringField('Last Name',validators=[DataRequired('Please enter you lastname')])
    submit = SubmitField('Login')

    class Meta:
        csrf = True
csrf_time_limit = 360

class Meta:
        csrf = True
csrf_time_limit = 360

class User_reg(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    pwd = PasswordField('Password', validators=[DataRequired('Password is required')])
    phone = TelField('Phone Number', validators=[DataRequired('Phone number is required')])
    file = FileField('Upload your picture')
    users = SelectField('Users', choices=[('Users'), ('Scorers')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 360

class Artist_Reg(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    file = FileField('Upload your picture')
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 360

