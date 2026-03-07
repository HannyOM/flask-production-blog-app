from flask_security.signals import user_registered
from . import db
from .models import Role


def setup_roles_signals(app):
    @user_registered.connect_via(app)
    def assign_default_role(sender, user, **extra):
        # Find the "user" role.
        role = Role.query.filter_by(name="reader").first()
        
        # Create "user" role if it doesn't exist.
        if not role:
            role = Role(name="reader", description="can only read posts.")
            db.session.add(role)
            db.session.commit()
            print("Created 'user' role in database.")

        # 3. Assign it to the user.
        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
            print(f"Assigned 'user' role to {user.email}")