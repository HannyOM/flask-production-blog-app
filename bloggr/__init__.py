import os
from dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore 
from flask_mail import Mail


load_dotenv()

# Instantiate extensions (without app object).
db = SQLAlchemy()                   
migrate = Migrate()
mail = Mail()

# Application factory
def create_app(test_config=None):
    app = Flask(__name__)           # Identifies the root path for resources like templates and static files.
    
    app.config.from_mapping(
        # Configure application.
        DEBUG = os.environ.get("DEBUG") == "1",
        SECRET_KEY = os.environ.get("SECRET_KEY"),
        # Configure Flask SQLAlchemy
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        # Configure Flask Security (General)
        SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT"),
        REMEMBER_COOKIE_SAMESITE = "strict",
        SESSION_COOKIE_SAMESITE = "strict",
        # Configure Flask Security (Registerable)
        SECURITY_REGISTERABLE = True,
        SECURITY_EMAIL_SUBJECT_REGISTER = os.environ.get("SECURITY_EMAIL_SUBJECT_REGISTER"),
        SECURITY_USERNAME_ENABLE = True,
        SECURITY_USERNAME_REQUIRED = True,
        # Configure Flask Security (Confirmable)
        SECURITY_CONFIRMABLE = True,
        SECURITY_POST_CONFIRM_VIEW = "/login",
        # Configure Flask Mail
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = os.environ.get("MAIL_USERNAME"),
        MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER"),
    )

    # Override with test_config if it exists.
    if test_config is not None:
        app.config.update(test_config)

    # Initialize extensions (with app object).
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import User model to create user table in database.
    from .models import User, Role

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Automatically assign registered user with "user" role.
    from .roles import setup_roles_signals
    setup_roles_signals(app)

    # Import blueprints
    from . import blog
    
    # Register blueprints
    app.register_blueprint(blog.bp)
    app.add_url_rule("/",
                     endpoint="index")          # Associates the endpoint name 'index' with the '/' url, so that url_for('index') or url_for('blog.index') will both work, generating the same / URL.

    return app