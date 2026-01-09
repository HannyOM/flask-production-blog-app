from . import db


class User(db.Model):            # Initializes a "User" table with three columns.
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
