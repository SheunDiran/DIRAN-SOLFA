from flask import Flask
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
load_dotenv()
app=Flask(__name__,template_folder='my_templates')
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
csrf = CSRFProtect()
csrf.init_app(app)
from packages import my_route,myforms