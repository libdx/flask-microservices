import os
from flask import Flask
from flask_restx import Resource, Api


app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


class Ping(Resource):

    '''Represents health check'''

    def get(self):
        '''GET /ping endpoint

        Returns
            dict object representing health status

        '''
        return {'status': 'success', 'message': 'pong'}


api.add_resource(Ping, '/ping')
