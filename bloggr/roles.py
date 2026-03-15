from flask_security.signals import user_registered
from flask import current_app
from . import db
from .models import Role
import logging

logger = logging.getLogger(__name__)


def setup_roles_signals(app):
    @user_registered.connect_via(app)
    def assign_default_role(sender, user, **extra):
        try:
            role = Role.query.filter_by(name="editor").first()

            if not role:
                role = Role(name="editor", description="can create and edit posts.")
                db.session.add(role)
                db.session.commit()
                role = Role.query.filter_by(name="editor").first()

            if role not in user.roles:
                user.roles.append(role)
                db.session.commit()
        except Exception as e:
            logger.error(f"Error assigning role to user {user.email}: {e}")
            db.session.rollback()
