from flask import Flask
from flask_migrate import Migrate
from packages import config
from flask_wtf import CSRFProtect


def create_app():
    from packages.models import db
    app=Flask(__name__,instance_relative_config=True,template_folder='my_templates')

    app.config.from_pyfile('config.py')
    csfr=CSRFProtect(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app

app=create_app()
from packages import user_forms,user_route,admin_route,json_route