from flask import request
from flask_restx import Namespace, Resource, fields

from project.api.users.crud import (
    add_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)

namespace = Namespace("users")

user = namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    """Represents /users endpoint"""

    @namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users."""
        return get_all_users(), 200

    @namespace.expect(user, validate=True)
    @namespace.response(201, "user <user_email> was created")
    @namespace.response(400, "user <user_email> already exists")
    def post(self):
        """Creates a new user."""

        payload = request.get_json()
        username = payload.get("username")
        email = payload.get("email")

        user = get_user_by_email(email)
        if not user:
            add_user(username, email)
            return {"message": f"user {email} was created", "status": "success"}, 201
        else:
            return {"message": f"user {email} already exists", "status": "failed"}, 400


class Users(Resource):
    """Represents /users/<user_id> endpoint"""

    @namespace.marshal_with(user)
    @namespace.response(200, "Success")
    @namespace.response(404, "User with id <user_id> does not exists")
    def get(self, user_id):
        """Returns a single user."""

        user = get_user_by_id(user_id)
        if not user:
            namespace.abort(404, f"User with id {user_id} does not exists")
        return user, 200

    @namespace.expect(user, validate=True)
    @namespace.response(200, "User with id <user_id> was updated")
    @namespace.response(404, "User with id <user_id> does not exists")
    @namespace.response(400, "Email is already taken")
    def put(self, user_id):
        """Updates the user."""

        payload = request.get_json()
        username = payload.get("username")
        email = payload.get("email")

        user = get_user_by_id(user_id)
        if not user:
            namespace.abort(404, f"User with id {user_id} does not exists")

        if get_user_by_email(email) != user:
            namespace.abort(400, f"{email} is already taken")

        update_user(user, username, email)

        return {"message": f"User {email} was updated", "status": "success"}, 200

    @namespace.response(200, "<user_id> was deleted")
    @namespace.response(404, "<user_id> does not exists")
    def delete(self, user_id):
        """Deletes the user.

        Args:
            user_id (int): numeric user identifier
        """

        user = get_user_by_id(user_id)
        if not user:
            namespace.abort(404, f"User with id {user_id} does not exists")
        delete_user(user)
        return {"message": f"{user.email} was deleted", "status": "success"}, 200


namespace.add_resource(UsersList, "")
namespace.add_resource(Users, "/<int:user_id>")
