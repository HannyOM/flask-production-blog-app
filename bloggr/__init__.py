import os
from flask import Flask
from dotenv import load_dotenv 

load_dotenv()
def create_app(test_config=None):
    app = Flask(__name__,                   # Tells the app the name of the current Python module where it is located.
                instance_relative_config=True )                 # Tells the app that the configuration files are relative to the instance folder.
    
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    return app