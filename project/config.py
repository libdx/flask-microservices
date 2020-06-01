class BaseConfig:
    '''Base configuration'''

    TESTIN = False


class DevelopmentConfig(BaseConfig):
    '''Configuration for Development environment'''


class TestingConfig(BaseConfig):
    '''Configuration for Testing environment'''

    TESTING = True


class ProductionConfig(BaseConfig):
    '''Configuration for Production environment'''
