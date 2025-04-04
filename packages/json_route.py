import json
from flask import render_template,flash,request,redirect,session
from packages import app
from packages.models import db,User

@app.route('/ajax/process/',methods=['POST',"GET"])
def check_details():
    email = request.form.get('email') 
    password = request.form.get('password') 
    phone_number = request.form.get('phone') 
    user_email=db.session.query(User).filter(User.users_email==email).count()
    user_password=db.session.query(User).filter(User.users_password==password).count()
    phonenumber=db.session.query(User).filter(User.users_phonenumber==phone_number).count()
    if user_email:
        return "Email address  is taken"
    elif user_password:
        return 'Password is not available'
    elif phonenumber:
        return 'Phone number is taken'
    else:
        return render_template('User/user_reg.html')