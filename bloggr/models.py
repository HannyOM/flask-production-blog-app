from . import db
from flask_security.core import UserMixin, RoleMixin


roles_users = db.Table(
    "roles_users", 
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"))
)

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):            # Initializes a "User" table with three columns.
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")) # type: ignore