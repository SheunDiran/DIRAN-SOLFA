from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TimeField,DateField,DateTimeLocalField,FileField
from wtforms.validators import DataRequired

class AdminForm(FlaskForm):
   username=StringField('Username',validators=[DataRequired('Enter your username')])
   pwd = PasswordField('Password', validators=[DataRequired('Enter your password')])
   date = DateTimeLocalField(' Login Date',validators=[DataRequired('Enter your login date and time')])
   submit = SubmitField('Login')        

class Meta:
        csrf = True
csrf_time_limit = 360

class Admin_Reg(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Enter your username')])
    pwd = PasswordField('Password', validators=[DataRequired('Enter your password')])
    file = FileField('Upload your picture')
    date = DateField('Registration Date', validators=[DataRequired('Enter the date')])
    submit = SubmitField('Register')

    class Meta:
        csrf = True
        csrf_time_limit = 360