from datetime import timedelta
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)


#Import configuration options from config.py
app.config.from_object('app.config')


app.permanent_session_lifetime = timedelta(minutes=720)

#create DB session
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

#needs instance first
from app import view, api_view
from model import User,Role




db.create_all()




