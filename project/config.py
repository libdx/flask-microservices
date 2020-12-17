import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 15 * 60  # 15min
    REFRESH_TOKEN_EXPIRATION = 30 * 24 * 60 * 60  # 30 days


class DevelopmentConfig(BaseConfig):
    """Configuration for Development environment"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Configuration for Testing environment"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    """Configuration for Production environment"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
