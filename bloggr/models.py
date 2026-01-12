from . import db
from flask_security.core import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


roles_users = db.Table(
    "roles_users", 
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"), primary_key=True),
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True)
)

# Creates a "Role" table with three columns.
class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(db.String(255))

# Creates a "User" table with five columns.
class User(db.Model, UserMixin):            
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True) 
    username: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    fs_uniquifier: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    roles: Mapped[List[Role]] = relationship(secondary=roles_users, backref="users")