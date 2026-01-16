from __future__ import annotations
from . import db
from flask_security.core import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime


# Roles-Users Core/Association table (Many To Many)
roles_users = db.Table(
    "roles_users", 
    db.Column("role_id", Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
    db.Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
)


# Creates a "Role" table with three columns.
class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)           # type: ignore
    name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)           # type: ignore
    description: Mapped[str | None] = mapped_column(db.String(255))           # type: ignore
    users: Mapped[List[User]] = relationship(secondary=roles_users, back_populates="roles")


# Creates a "User" table with five columns.
class User(db.Model, UserMixin):            
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)           # type: ignore
    username: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)           # type: ignore
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)           # type: ignore
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)           # type: ignore
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)           # type: ignore
    active: Mapped[bool] = mapped_column(default=True)           # type: ignore
    fs_uniquifier: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)           # type: ignore
    roles: Mapped[List[Role]] = relationship(secondary=roles_users, back_populates="users")           # type: ignore