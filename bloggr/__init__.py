import os
from dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore 
# from flask_security.decorators import auth_required
# from flask_security.utils import hash_password
from flask_mail import Mail


load_dotenv()

# Instantiate extensions (without app object).
db = SQLAlchemy()                   
migrate = Migrate()
mail = Mail()

# Application factory
def create_app(test_config=None):
    app = Flask(__name__)           # Identifies the root path for resources like templates and static files.
    
    # Configure application.
    app.config["DEBUG"] = os.environ.get("DEBUG") == "1"
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    # Configure Flask SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Configure Flask Security(General)
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
    app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
    app.config["SESSION_COOKIE_SAMESITE"] = "strict"
    # Configure Flask Security(Registerable)
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_EMAIL_SUBJECT_REGISTER"] = "User Registration"
    app.config["SECURITY_USERNAME_ENABLE"] = True
    app.config["SECURITY_USERNAME_REQUIRED"] = True
    # Configure Flask Security(Confirmable)
    app.config["SECURITY_CONFIRMABLE"] = True
    app.config["SECURITY_POST_CONFIRM_VIEW"] = "auth/register.html"
    # Configure Flask Mail
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

    # Initialize extensions (with app object).
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import User model to create user table in database.
    from .models import User, Role

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    return app