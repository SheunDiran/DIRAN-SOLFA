from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,SelectField
from wtforms import TextAreaField,FileField,RadioField
from wtforms.validators import DataRequired,Email,Optional
from flask_wtf.file import FileField,FileRequired,FileAllowed

class UploadDpForm(FlaskForm):
    picture=FileField(validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'ONLY IMAGES ARE ALLOWED')])
    upload=SubmitField('Upload Picture')

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
    users = SelectField('Role(User/Scorer)', choices=[('Users'), ('Scorers')])
    instrument = SelectField('Instrument', coerce=int, validators=[DataRequired('Please select an instrument')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 3600


class Artist_Reg(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    file = FileField('Upload your picture')
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 360

class AddSongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired()])
    song_lyrics = TextAreaField('Song Lyrics', validators=[DataRequired()])
    selection = RadioField('Select', choices=[('artist', 'Artist'), ('scorer', 'Scorer')])
    artist_id = SelectField('Artist', coerce=int, validators=[Optional()])
    scorer_id = SelectField('Scorer', coerce=int, validators=[Optional()])
    solfa_notation = TextAreaField('Solfa Notation', validators=[DataRequired()])
    



    

class Edit_User(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    phone = StringField('Phone Number')
    instrument = SelectField('Instrument', coerce=int)
    instrument_type = SelectField('Instrument Type', coerce=int)
    submit = SubmitField('Update')

    class Meta:
        csrf = True
        csrf_time_limit = 3600