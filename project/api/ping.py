from flask import Blueprint
from flask_restx import Resource, Api

blueprint = Blueprint('ping', __name__)
api = Api(blueprint)


class Ping(Resource):
    '''Represents health check'''

    def get(self):
        '''GET /ping endpoint

        Returns
            dict object representing health status

        '''
        return {'status': 'success', 'message': 'pong'}


api.add_resource(Ping, '/ping')
