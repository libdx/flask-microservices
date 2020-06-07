from flask import Blueprint
from flask_restx import Api, Resource

ping_blueprint = Blueprint('ping', __name__)
api = Api(ping_blueprint)


class Ping(Resource):
    '''Represents health check'''

    def get(self):
        '''GET /ping endpoint

        Returns:
            dict object representing health status

        '''
        return {'status': 'success', 'message': 'pong'}


api.add_resource(Ping, '/ping')
