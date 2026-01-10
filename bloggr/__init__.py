import os
from dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


load_dotenv()

# Instantiate extensions (without app object).
db = SQLAlchemy()                   
migrate = Migrate()

# Application factory
def create_app(test_config=None):
    app = Flask(__name__)           # Identifies the root path for resources like templates and static files.
    
    # Configure application.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions (with app object).
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import User

    return app