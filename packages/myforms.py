from flask_wtf import FlaskForm
from wtforms import RadioField,StringField, PasswordField, SubmitField,EmailField,SelectField
from wtforms import DateTimeLocalField,FileField
from wtforms.validators import DataRequired,Email


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    pwd = PasswordField('Password', validators=[DataRequired('Password is required')])
    date = DateTimeLocalField(' Login Date',validators=[DataRequired('Enter your login date')])
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

class AdminForm(FlaskForm):
   username=StringField('Username',validators=[DataRequired('Enter your username')])
   pwd = PasswordField('Password', validators=[DataRequired('Enter your password')])
   date = DateTimeLocalField(' Login Date',validators=[DataRequired('Enter your login date and time')])
   submit = SubmitField('Login')        

class Meta:
        csrf = True
csrf_time_limit = 360

class User_reg(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired('Please enter you firstname')])
    lname = StringField('Last Name',validators=[DataRequired('Please enter you lastname')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    pwd = PasswordField('Password', validators=[DataRequired('Password is required')])
    phone=StringField('Phone Number',validators=[DataRequired('Phone number is required')])
    date = DateTimeLocalField('Date',validators=[DataRequired('Enter your login date')])
    file=FileField('Upload your picture')
    file2=FileField('Upload your CV/Work')
    users = SelectField('Users', choices=[('Users'), ('Scorers')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
csrf_time_limit = 360
     


class Artist_Reg(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired('Please enter you firstname')])
    lname = StringField('Last Name',validators=[DataRequired('Please enter you lastname')])
    file=FileField('Upload your picture')
    pwd = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
csrf_time_limit = 360


class Admin_Reg(FlaskForm):
   username=StringField('Username',validators=[DataRequired('Enter your username')])
   pwd = PasswordField('Password', validators=[DataRequired('Enter your password')])
   file=FileField('Upload your picture')
   date = DateTimeLocalField(' Registration Date',validators=[DataRequired('Enter the date and time')])
   submit = SubmitField('Register')        

class Meta:
        csrf = True
csrf_time_limit = 360