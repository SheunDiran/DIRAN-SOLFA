from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,TextAreaField
from wtforms.validators import DataRequired,Email
from flask_wtf.file import FileField,FileRequired,FileAllowed

class DpForm(FlaskForm):
    photo=FileField(validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'ONLY IMAGES ARE ALLOWED')])
    uploadbtn=SubmitField('Upload Picture')


class AdminLogin(FlaskForm):
    username = EmailField('Username', validators=[DataRequired('Username is required')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Login')

    class Meta:
        csrf = True
csrf_time_limit = 360


class SongForm(FlaskForm):
    artist = StringField('Artist Name')
    song_title = StringField('Song Title', validators=[DataRequired('Please song title is required')])
    song_lyrics = TextAreaField('Song Lyrics', validators=[DataRequired("Please song lyrics is required")])
    solfa_notation = TextAreaField('Solfa Notation')
    submit = SubmitField('Save Changes')




      

