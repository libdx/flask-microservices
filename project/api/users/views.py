from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from project.api.users.crud import (
    add_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
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

    @api.marshal_with(user, as_list=True)
    def get(self):
        return get_all_users(), 200

    @api.expect(user, validate=True)
    def post(self):
        """POST /users"""

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

    @api.marshal_with(user)
    def get(self, user_id):
        """GET /user/:id"""

        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User with id {user_id} does not exists")
        return user, 200

    @api.expect(user, validate=True)
    def put(self, user_id):
        """PUT /user/:id"""
        payload = request.get_json()
        username = payload.get("username")
        email = payload.get("email")

        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User with id {user_id} does not exists")

        update_user(user, username, email)

        return {"message": f"User {email} was updated", "status": "success"}, 200

    def delete(self, user_id):
        """DELETE /user/:id
        Args:
            user_id: int numeric user identifier
        """
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User with id {user_id} does not exists")
        delete_user(user)
        return {"message": f"{user.email} was deleted", "status": "success"}


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
