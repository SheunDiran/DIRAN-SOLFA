from flask import Flask
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
load_dotenv()
app=Flask(__name__,instance_relative_config=True,template_folder='my_templates')
app.config.from_pyfile('config.py')
csrf = CSRFProtect()
csrf.init_app(app)
from packages import user_forms,user_route,admin_forms,admin_route