from flask import Flask
from assembly22.config import Config
from assembly22.models import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


from views import *
