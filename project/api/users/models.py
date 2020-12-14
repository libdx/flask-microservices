import os

from sqlalchemy.sql import func

from project import db


class User(db.Model):
    """User representation"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        """Initializes User with username and email

        Args:
            username: string represents unique human readable identifier
            email: string represents unique email address

        """
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User {self.id} {self.email}"


if os.getenv("FLASK_ENV") == "development":
    from project import admin
    from project.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
