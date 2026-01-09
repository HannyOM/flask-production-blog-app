import os
from flask import Flask
from dotenv import load_dotenv 
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()                   # Initializes without the app.

def create_app(test_config=None):
    app = Flask(__name__,                   # Tells the app the name of the current Python module where it is located.
                instance_relative_config=True )                 # Tells the app that the configuration files are relative to the instance folder.
    
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models import User

    return app