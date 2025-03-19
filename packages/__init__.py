from flask import Flask

app=Flask(__name__,template_folder='my_templates')

from packages import my_route