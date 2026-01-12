import os
from dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore 
from flask_security.decorators import auth_required
from flask_security.utils import hash_password


load_dotenv()

# Instantiate extensions (without app object).
db = SQLAlchemy()                   
migrate = Migrate()

# Application factodry
def create_app(test_config=None):
    app = Flask(__name__)           # Identifies the root path for resources like templates and static files.
    
    # Configure application.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
    app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
    app.config["SESSION_COOKIE_SAMESITE"] = "strict"
    
    # Initialize extensions (with app object).
    db.init_app(app)
    migrate.init_app(app, db)

    # Import User model to create user table in database.
    from .models import User, Role

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    return app