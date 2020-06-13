from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from project import db
from project.api.models import User

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

user = api.model(
    'User',
    {
        'id': fields.Integer(readOnly=True),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'created_date': fields.DateTime,
    },
)


class UsersList(Resource):
    '''Represents /users endpoint'''

    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200

    @api.expect(user, validate=True)
    def post(self):
        '''POST /users'''

        payload = request.get_json()
        username = payload.get('username')
        email = payload.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            return {'message': f'user {email} was created', 'status': 'success'}, 201
        else:
            return {'message': f'user {email} already exists', 'status': 'failed'}, 400


class Users(Resource):
    '''Represents /users/<user_id> endpoint'''

    @api.marshal_with(user)
    def get(self, user_id):
        '''GET /user/:id'''

        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f'User with id {user_id} does not exists')
        return user, 200

    @api.expect(user, validate=True)
    def put(self, user_id):
        '''PUT /user/:id'''
        payload = request.get_json()
        username = payload.get('username')
        email = payload.get('email')

        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f'User with id {user_id} does not exists')

        user.username = username
        user.email = email

        db.session.commit()

        return {'message': f'User {email} was updated', 'status': 'success'}, 200

    def delete(self, user_id):
        '''DELETE /user/:id
        Args:
            user_id: int numeric user identifier
        '''
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f'User with id {user_id} does not exists')
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{user.email} was deleted', 'status': 'success'}


api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')
