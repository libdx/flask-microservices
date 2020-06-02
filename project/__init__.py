import os
from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)


class User(db.Model):
    '''User representation'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        '''Initializes User with username and email

        username:
            string represents unique human readable identifier
        email:
            string represents unique email address

        '''
        self.username = username
        self.email = email


class Ping(Resource):

    '''Represents health check'''

    def get(self):
        '''GET /ping endpoint

        Returns
            dict object representing health status

        '''
        return {'status': 'success', 'message': 'pong'}


api.add_resource(Ping, '/ping')
