import jwt
from flask import request
from flask_restx import Namespace, Resource, fields

from project.api.users.crud import add_user, get_user_by_email, get_user_by_id
from project.api.users.models import User

namespace = Namespace("auth")

user_result = namespace.model(
    "User Result",
    {"username": fields.String(required=True), "email": fields.String(required=True)},
)

user_payload = namespace.clone(
    "User Payload", user_result, {"password": fields.String(required=True)}
)

login = namespace.model(
    "User",
    {"email": fields.String(required=True), "password": fields.String(required=True)},
)

refresh = namespace.model("Refresh", {"refresh_token": fields.String(required=True)})

tokens = namespace.clone(
    "Access and Refresh Tokens", refresh, {"access_token": fields.String(required=True)}
)

status_parser = namespace.parser()
status_parser.add_argument("Authorization", location="headers")


class Register(Resource):
    @namespace.marshal_with(user_result)
    @namespace.expect(user_payload, validate=True)
    @namespace.response(201, "Success")
    @namespace.response(400, "User with given email already exists")
    def post(self):
        """Register and returns new user."""
        payload = request.get_json()
        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")

        user = get_user_by_email(email)
        if user:
            namespace.abort(400, f"User with email {email} already exists")
        user = add_user(username, email, password)

        return user, 201


class Login(Resource):
    @namespace.marshal_with(tokens)
    @namespace.expect(login)
    @namespace.response(200, "Success")
    @namespace.response(401, "User with given email or password does not exists")
    def post(self):
        """Validates credentials and returns access and refresh tokens on success."""

        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")

        user = get_user_by_email(email)
        if not user or not user.check_password(password):
            namespace.abort(
                401, f"User with given email {email} or password does not exists"
            )

        access_token = User.encode_token(user.id, "access").decode()
        refresh_token = User.encode_token(user.id, "refresh").decode()

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


class Refresh(Resource):
    @namespace.marshal_with(tokens)
    @namespace.expect(refresh, validate=True)
    @namespace.response(200, "Success")
    @namespace.response(401, "Invalid token")
    def post(self):
        """Creates new Access and Refresh tokens."""
        payload = request.get_json()
        refresh_token = payload.get("refresh_token")

        try:
            user_id = User.decode_token(refresh_token)

            user = get_user_by_id(user_id)
            if not user:
                namespace.abort(401, "Invalid token")

            access_token = User.encode_token(user.id, "access").decode()
            refresh_token = User.encode_token(user.id, "refresh").decode()

            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        except jwt.ExpiredSignature:
            namespace.abort(401, "Token expired")
        except jwt.InvalidTokenError:
            namespace.abort(401, "Invalid token")


class Status(Resource):
    @namespace.marshal_with(user_result)
    @namespace.response(200, "Success")
    @namespace.response(401, "Invalid Token")
    @namespace.expect(status_parser)
    def get(self):
        auth_header = request.headers.get("Authorization") or ""
        if auth_header:
            try:
                access_token = auth_header.split(" ")[1]
                user_id = User.decode_token(access_token)
                user = get_user_by_id(user_id)
                if not user:
                    namespace.abort(401, "Invalid token")

                return user, 200
            except jwt.ExpiredSignatureError:
                namespace.abort(401, "Token expired")
            except jwt.InvalidTokenError:
                namespace.abort(401, "Invalid token")
            except IndexError:
                namespace.abort(401, "Invalid token")
        else:
            namespace.abort(403, "Access token required")


namespace.add_resource(Register, "/register")
namespace.add_resource(Login, "/login")
namespace.add_resource(Refresh, "/refresh")
namespace.add_resource(Status, "/status")
