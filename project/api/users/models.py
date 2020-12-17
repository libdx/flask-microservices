import datetime
import os

import jwt
from flask import current_app
from sqlalchemy.sql import func

from project import bcrypt, db

# TODO: invalidate refresh tokens
# storing single refresh token per user in database (create separate table)


class User(db.Model):
    """User representation"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password=""):
        """Initializes User with username and email

        Args:
            username: string represents unique human readable identifier
            email: string represents unique email address

        """
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()

    def __repr__(self):
        return f"User {self.id} {self.email}"

    def check_password(self, password):
        """Tests given password agains user's password."""
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def encode_token(user_id, token_type="access"):
        """Creates JWT token.

        Args:
            user_id (int): user identifier.
            token_type (str): type of the token: "access" or "refresh".
                Default is "access".

        Returns:
            token (bytes): encoded JWT token.
        """
        if token_type == "access":
            timedelta_seconds = current_app.config["ACCESS_TOKEN_EXPIRATION"]
        else:
            timedelta_seconds = current_app.config["REFRESH_TOKEN_EXPIRATION"]

        payload = {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(days=0, seconds=timedelta_seconds),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        secret_key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token):
        """Decodes token returning user id.

        Args:
            token (Union[str, bytes]): access or refresh token created by
                :meth: User.encode_token.

        Returns:
            user_id (int): user identifier.
        """
        payload = jwt.decode(token, current_app.config["SECRET_KEY"])
        return payload["sub"]


if os.getenv("FLASK_ENV") == "development":
    from project import admin
    from project.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
