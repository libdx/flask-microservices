import os


class BaseConfig:
    '''Base configuration'''

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'


class DevelopmentConfig(BaseConfig):
    '''Configuration for Development environment'''

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    '''Configuration for Testing environment'''

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    '''Configuration for Production environment'''

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
